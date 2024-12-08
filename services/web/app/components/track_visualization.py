import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, no_update
from util import get_data
import plotly.express as px

telemetry_options = [
    {"label": "Speed", "value": "Speed"},
    {"label": "nGear", "value": "nGear"},
    {"label": "RPM", "value": "RPM"},
    {"label": "Throttle", "value": "Throttle"},
    {"label": "Brake", "value": "Brake"},
]
telemetry_types = [x["label"] for x in telemetry_options]

track_graph_driver_dropdown = html.Div(
    children=[
        dcc.Checklist(
            id="tv-driver-dropdown",
            inline=True,
        )
    ],
    id="driver-dropdown-div",
)

track_graph = html.Div(id="track-graph")

selected_driver_label = html.Div(id="selected-driver-label")


def make_layout():
    return dbc.Row(
        children=[
            dbc.Row(children=[html.H1(children="Driver Telemetry")]),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        [
                                            html.H5("Select up to 2 drivers:"),
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
                                    html.H5("Select telemetry:"),
                                    dcc.Dropdown(
                                        id="telemetry-dropdown",
                                        options=telemetry_options,
                                        value="Speed",
                                        clearable=False,
                                    ),
                                    dbc.Row(
                                        children=[
                                            html.Div(
                                                style={
                                                    "margin": "0.35em",
                                                    "padding": "0.35em",
                                                }
                                            )
                                        ]
                                    ),
                                    selected_driver_label,
                                    track_graph,
                                ]
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )


@callback(
    Output("tv-driver-dropdown", "options"),
    Input("tv-driver-dropdown", "options"),
    Input("tv-driver-dropdown", "value"),
)
def tv_driver_dropdown_checkboxes(driver_options, selected_values):
    if not driver_options:
        return no_update
    if not selected_values:
        return no_update

    if len(selected_values) >= 2:
        temp_vals = []
        driver_numbers = [val["DriverNumber"] for val in selected_values]
        for opt in driver_options:
            disabled = False
            if opt["value"]["DriverNumber"] not in driver_numbers:
                disabled = True
            temp_vals.append(
                {"label": opt["label"], "value": opt["value"], "disabled": disabled}
            )
        return temp_vals
    else:
        return [
            {"label": opt["label"], "value": opt["value"], "disabled": False}
            for opt in driver_options
        ]


@callback(
    Output("driver-dropdown-div", "children"),
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
        driver_options.append(
            {"label": driver_label_list, "value": driver, "disabled": False}
        )
    #
    children = [
        dcc.Checklist(
            options=driver_options,
            id="tv-driver-dropdown",
            inline=True,
        )
    ]
    return children


@callback(
    Output("track-graph", "children"),
    Output("selected-driver-label", "children"),
    Input("tv-driver-dropdown", "value"),
    Input("tv-driver-dropdown", "options"),
    Input("telemetry-dropdown", "value"),
    Input("RoundNumber_dropdown", "value"),
)
def update_graph(selected_driver, driver_options, selected_telemetry, event):
    if not selected_telemetry:
        selected_telemetry = "Speed"

    hover_dict = {
        "X": False,
        "Y": False,
        "Driver": True,
        "Speed": True,
        "nGear": True,
        "RPM": True,
        "Throttle": True,
        "Brake": True,
    }

    def get_driver_tel_df(event: int, selected_driver_number_list: list):
        driver_string = "(" + ",".join(selected_driver_number_list) + ")"
        with open("sql/get_event_driver_telemetry.sql") as f:
            query = f.read()
        df = get_data.get_data(
            query.format(EventNumber=event, DriverNumbers=driver_string)
        )
        return df

    if not selected_driver:
        selected_driver = [str(1)]
        driver_string = "(" + ",".join(selected_driver) + ")"
        with open("sql/get_event_plot.sql") as f:
            query = f.read()
        driver_laps = get_data.get_data(
            query.format(EventNumber=event, DriverNumbers=driver_string)
        )
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        fig = px.scatter(
            driver_laps,
            x="X",
            y="Y",
            color="Sector",
            title="Track with Sectors",
            render_mode="scattergl",
            hover_data={"X": False, "Y": False, "Sector": True},
        )

        fig.update_traces(line=dict(width=5))
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgb(229,229,229)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
        )

        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        return [dcc.Graph(figure=fig)], dbc.Row(
            children=[html.H5("No driver selected")]
        )

    elif len(selected_driver) == 1:
        driver_laps = get_driver_tel_df(
            event, [str(selected_driver[0]["DriverNumber"])]
        )
        if driver_laps.empty:
            fig = px.line(title=f"No data available for driver {selected_driver}")
            return [dcc.Graph(figure=fig)], dbc.Row(
                children=[
                    dbc.Col(children=[html.H5(f"{selected_driver[0]['FullName']}")])
                ]
            )
        # Not in sql for performance reasons
        driver_laps["Driver"] = selected_driver[0]["FullName"]

        fig = px.scatter(
            driver_laps,
            x="X",
            y="Y",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            title="Track with Sectors",
            render_mode="scattergl",
            hover_data=hover_dict,
        )

        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgb(229,229,229)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
        )

        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        return [dcc.Graph(figure=fig)], dbc.Row(
            children=[dbc.Col(children=[html.H5(f"{selected_driver[0]['FullName']}")])]
        )

    elif len(selected_driver) >= 2:
        tel = get_driver_tel_df(
            event,
            [
                str(selected_driver[0]["DriverNumber"]),
                str(selected_driver[1]["DriverNumber"]),
            ],
        )
        tel_d1 = tel[tel["DriverNumber"] == selected_driver[0]["DriverNumber"]]
        tel_d2 = tel[tel["DriverNumber"] == selected_driver[1]["DriverNumber"]]

        # tel_d1 = get_driver_tel_df(event, [str(selected_driver[0]["DriverNumber"])])
        # tel_d2 = get_driver_tel_df(event, [str(selected_driver[1]["DriverNumber"])])

        tel_d1.loc[:, "Driver"] = selected_driver[0]["FullName"]
        tel_d2.loc[:, "Driver"] = selected_driver[1]["FullName"]

        fig1 = px.scatter(
            tel_d1,
            x="X",
            y="Y",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            title=None,
            render_mode="scattergl",
            hover_data=hover_dict,
        )

        fig2 = px.scatter(
            tel_d2,
            x="X",
            y="Y",
            color=selected_telemetry,
            color_continuous_scale="Pinkyl",
            title=None,
            render_mode="scattergl",
            hover_data=hover_dict,
        )

        fig1.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgb(229,229,229)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig1.update_yaxes(scaleanchor="x", scaleratio=1)
        fig1.update_coloraxes(showscale=False)

        fig2.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgb(229,229,229)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig2.update_yaxes(scaleanchor="x", scaleratio=1)

        return [
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(figure=fig1)),
                    dbc.Col(dcc.Graph(figure=fig2)),
                ]
            )
        ], dbc.Row(
            children=[
                dbc.Col(children=[html.H5(f"{selected_driver[0]['FullName']}")]),
                dbc.Col(children=[html.H5(f"{selected_driver[1]['FullName']}")]),
            ]
        )
