import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
from util import get_data
import pandas as pd
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
                                        value=telemetry_options[0],
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


# @callback(
#     Output("selected-driver-label", "children"),
#     Input("tv-driver-dropdown", "value"),
# )
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
    [Output("tv-driver-dropdown", "options")],
    Input("RoundNumber_dropdown", "value"),
)
def update_current_event(event):
    if not event:
        return [{"label": "hello", "value": 1}]
    with open("sql/get_event_drivers_tv.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(EventNumber=event))

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
        driver_options.append(
            {"label": driver_label_list, "value": driver["DriverNumber"]}
        )

    return driver_options


@callback(
    Output("tv-driver-dropdown", "options"),
    Input("tv-driver-dropdown", "value"),
    Input("tv-driver-dropdown", "options"),
)
def update_multi_options(value, driver_options):
    options = driver_options
    if not value:
        return options
    if len(value) >= 2:
        options = [
            {
                "label": option["label"],
                "value": option["value"],
                "disabled": option["value"] not in value,
            }
            for option in options
        ]
    return options


# @callback(
#     Output("track-graph", "figure"),
#     Input("tv-driver-dropdown", "value"),
#     Input("telemetry-dropdown", "value"),
#     Input("RoundNumber_dropdown", "value"),
# )
def update_graph(selected_driver, selected_telemetry, event):
    if not selected_telemetry:
        selected_telemetry = "Speed"

    print(selected_driver)
    with open("sql/get_event_driver_telemetry.sql") as f:
        query = f.read()
    df = get_data.get_data(
        query.format(EventNumber=event, DriverNumber=selected_driver)
    )

    if not selected_driver:
        selected_driver = str(drivers[:1])
        driver_laps = pd.DataFrame.from_dict(
            current_event[selected_driver], orient="columns"
        )
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        fig = px.line(
            driver_laps,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title="Track with Sectors",
        )

        fig.update_traces(line=dict(width=5))

    elif len(selected_driver) == 1:
        driver_laps = pd.DataFrame.from_dict(
            current_event[selected_driver], orient="columns"
        )
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        scale_in = -250.0
        subj = tuple(driver_laps[["X", "Y"]].itertuples(index=False, name=None))
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(subj, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        solution = pco.Execute(scale_in)

        df = pd.DataFrame(solution[0], columns=["X_prime", "Y_prime"])

        # for all points in df, compute min distance
        df["Original_Row"] = [
            np.argmin(np.linalg.norm(row - driver_laps[["X", "Y"]], axis=1))
            for row in df.itertuples(index=False, name=None)
        ]
        df[selected_telemetry] = [
            driver_laps.iloc[n][selected_telemetry] for n in df["Original_Row"]
        ]

        fig1 = px.line(
            driver_laps,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title=f"Track with Sectors",
        )

        fig2 = px.scatter(
            df,
            x="X_prime",
            y="Y_prime",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            render_mode="webgl",
        )

        fig1.update_traces(line=dict(width=5))
        fig = go.Figure(data=fig1.data + fig2.data)

    elif len(selected_driver) == 2:
        tel_d1 = pd.DataFrame.from_dict(
            current_event[selected_driver], orient="columns"
        )
        tel_d2 = pd.DataFrame.from_dict(
            current_event[selected_driver], orient="columns"
        )

        scale_in = -250.0
        subj = tuple(tel_d1[["X", "Y"]].itertuples(index=False, name=None))
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(subj, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        solution = pco.Execute(scale_in)

        df_in = pd.DataFrame(solution[0], columns=["X_prime", "Y_prime"])

        # for all points in df, compute min distance
        df_in["Original_Row"] = [
            np.argmin(np.linalg.norm(row - tel_d1[["X", "Y"]], axis=1))
            for row in df_in.itertuples(index=False, name=None)
        ]
        df_in[selected_telemetry] = [
            tel_d1.iloc[n][selected_telemetry] for n in df_in["Original_Row"]
        ]

        scale_out = 250.0
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

        fig1 = px.line(
            tel_d1,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title="Track with Sectors",
        )

        fig2 = px.scatter(
            df_in,
            x="X_prime",
            y="Y_prime",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            render_mode="webgl",
        )

        fig3 = px.scatter(
            df_out,
            x="X_prime",
            y="Y_prime",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            render_mode="webgl",
        )

        fig1.update_traces(line=dict(width=5))
        fig = go.Figure(data=fig1.data + fig2.data + fig3.data)

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
