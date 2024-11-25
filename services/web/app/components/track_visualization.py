import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, no_update
from util import get_data
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pyclipper

telemetry_options = [
    {"label": "Speed", "value": "Speed"},
    {"label": "nGear", "value": "nGear"},
    {"label": "RPM", "value": "RPM"},
    {"label": "Throttle", "value": "Throttle"},
    {"label": "Brake", "value": "Brake"},
]

track_graph_driver_dropdown = dcc.Checklist(
    options=[],
    value=[],
    id="tv-driver-dropdown",
    inline=True,
)

track_graph = dcc.Graph(id="track-graph")

selected_driver_label = html.Div(id="selected-driver-label")


def make_layout():
    return dbc.Row(
        children=[
            dbc.Row(children=[html.H1(children="F1 Track with Segments")]),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        [
                                            html.Label("Select driver:"),
                                            track_graph_driver_dropdown,
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                    dbc.Col(
                        children=[
                            html.Div(
                                [
                                    selected_driver_label,
                                    track_graph,
                                    html.Label("Select telemetry:"),
                                    dcc.Dropdown(
                                        id="telemetry-dropdown",
                                        options=telemetry_options,
                                        value=1,
                                        clearable=False,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )


@callback(
    Output("selected-driver-label", "children"),
    Input("tv-driver-dropdown", "value"),
)
def update_selected_driver_label(value):
    if not value:
        return dbc.Row(children=[html.Span("No driver selected")])
    elif len(value) == 1:
        return dbc.Row(
            children=[
                dbc.Col(children=[html.Span(f"Inner Driver: {value[0]['FullName']}")])
            ]
        )
    else:
        return dbc.Row(
            children=[
                dbc.Col(children=[html.Span(f"Inner Driver: {value[0]['FullName']}")]),
                dbc.Col(children=[html.Span(f"Outer Driver: {value[1]['FullName']}")]),
            ]
        )


@callback(
    Output("tv-driver-dropdown", "options"),
    Input("RoundNumber_dropdown", "value"),
)
def update_current_event(event):
    if not event:
        return [{"label": "hello", "value": 1}]
    with open("sql/get_event_drivers_tv.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(EventNumber=event))
    #
    driver_options = list()
    for driver in df.to_dict(orient="records"):
        driver_name = f"{driver['FullName']}"
        driver_position = f"{driver['ClassifiedPosition']}"
        driver_label_list = [
            html.Div(
                children=[
                    html.Img(src=driver["HeadshotUrl"], style={"padding": 5}),
                    html.Div(
                        driver_position,
                        style={
                            "font-size": 32,
                            "position": "absolute",
                            "top": "1px",
                            "left": "2px",
                            "color": "white",
                            "text-shadow": "-1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black, 1px 1px 0 black",
                        },
                    ),
                    html.Br(),
                    html.Span(
                        driver_name,
                        style={"font-size": 15, "padding": 5, "color": "black"},
                    ),
                ],
                style={"padding": 3, "position": "relative", "text-align": "center"},
            )
        ]
        driver_options.append({"label": driver_label_list, "value": driver})
    #
    return driver_options


# @callback(
#     Output("tv-driver-dropdown", "options"),
#     Input("tv-driver-dropdown", "value"),
#     Input("tv-driver-dropdown", "options"),
# )
def update_multi_options(value, driver_options):
    if not driver_options:
        return no_update
    if not value:
        return no_update

    if len(value) >= 2:
        # Disable options not selected
        return [
            {
                "label": opt["label"],
                "value": opt["value"],
                "disabled": opt["value"] not in value,
            }
            for opt in driver_options
        ]
    else:
        # Enable all options
        return [
            {"label": opt["label"], "value": opt["value"], "disabled": False}
            for opt in driver_options
        ]


@callback(
    Output("track-graph", "figure"),
    Input("tv-driver-dropdown", "value"),
    Input("tv-driver-dropdown", "options"),
    Input("telemetry-dropdown", "value"),
    Input("RoundNumber_dropdown", "value"),
)
def update_graph(selected_driver, driver_options, selected_telemetry, event):
    SCALE_OUT = 20.0
    if not selected_telemetry:
        selected_telemetry = "Speed"

    def get_driver_tel_df(event: int, selected_driver_number_list: list):
        driver_string = "(" + ",".join(selected_driver_number_list) + ")"
        with open("sql/get_event_driver_telemetry.sql") as f:
            query = f.read()
        df = get_data.get_data(
            query.format(EventNumber=event, DriverNumbers=driver_string)
        )
        return df

    if not selected_driver:
        selected_driver = [str(driver_options[0]["value"]["DriverNumber"])]
        driver_laps = get_driver_tel_df(event, selected_driver)
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        fig = px.scatter(
            driver_laps,
            x="X",
            y="Y",
            color="Sector",
            title="Track with Sectors",
        )

        fig.update_traces(line=dict(width=5))

    elif len(selected_driver) == 1:
        driver_laps = get_driver_tel_df(
            event, [str(selected_driver[0]["DriverNumber"])]
        )
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        fig = px.scatter(
            driver_laps,
            x="X",
            y="Y",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            title=f"Track with Sectors",
        )

    elif len(selected_driver) >= 2:
        tel_d1 = get_driver_tel_df(event, [str(selected_driver[0]["DriverNumber"])])
        tel_d2 = get_driver_tel_df(event, [str(selected_driver[1]["DriverNumber"])])

        scale_out = SCALE_OUT
        subj = tuple(tel_d2[["X", "Y"]].itertuples(index=False, name=None))
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(subj, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        solution = pco.Execute(scale_out)

        df_out = pd.DataFrame(solution[0], columns=["X_prime", "Y_prime"])

        # for all points in df, compute min distance
        df_out["Original_Row"] = [
            np.argmin(np.linalg.norm(row - tel_d2[["X", "Y"]], axis=1))
            for row in df_out.itertuples(index=False, name=None)
        ]
        df_out[selected_telemetry] = [
            tel_d2.iloc[n][selected_telemetry] for n in df_out["Original_Row"]
        ]

        fig1 = px.scatter(
            tel_d1,
            x="X",
            y="Y",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            render_mode="webgl",
            title="Track with Sectors",
        )

        fig2 = px.scatter(
            df_out,
            x="X_prime",
            y="Y_prime",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            render_mode="webgl",
        )

        fig = go.Figure(data=fig1.data + fig2.data)

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,1)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig
