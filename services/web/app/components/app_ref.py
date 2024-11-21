import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pyclipper
from .components import navbar
import fastf1 as f1
import os
import psycopg2

f1.Cache.enable_cache("/usr/src/app/cache")


event_query = """
SELECT * FROM "Events"; """

with psycopg2.connect(
    f"host={PGHOST} port={PGPORT} user={PGUSER} password={PGPASSWORD} dbname={PGDBNAME}"
) as conn:
    event_df = pd.read_sql_query(event_query, conn)

telemetry_options = [
    {"label": "Speed", "value": "Speed"},
    {"label": "nGear", "value": "nGear"},
    {"label": "RPM", "value": "RPM"},
    {"label": "Throttle", "value": "Throttle"},
    {"label": "Brake", "value": "Brake"},
]

current_event_store = dcc.Store(
    id={"type": "storage", "index": "current-event"}, storage_type="session"
)
driver_options_store = dcc.Store(
    id={"type": "storage", "index": "driver-options"}, storage_type="session"
)
driver_options_store = dcc.Store(
    id={"type": "storage", "index": "driver-options"}, storage_type="session"
)

year = 2024
event = 1
race = "Race"
session = f1.get_session(year, event, race)
session.load()
drivers = session.drivers

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])
server = app.server

events = event_df.to_dict(orient="records")

dcc.Store(id={"type": "storage", "index": "session"}, storage_type="session")

driver_number_fullname_map = {}

driver_options = list()
for driver in drivers:
    driver_info = session.get_driver(driver)
    driver_number_fullname_map[driver] = driver_info["FullName"]
    driver_name = f"{driver_info['FullName']}"
    driver_position = f"{driver_info['ClassifiedPosition']}"
    driver_label_list = [
        html.Div(
            children=[
                html.Img(src=driver_info["HeadshotUrl"], style={"padding": 5}),
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
                    driver_name, style={"font-size": 15, "padding": 5, "color": "black"}
                ),
            ],
            style={"padding": 3, "position": "relative", "text-align": "center"},
        )
    ]
    driver_options.append({"label": driver_label_list, "value": driver})


track_vis = dbc.Row(
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
                                        dcc.Checklist(
                                            id="driver-dropdown",
                                            options=driver_options,
                                            inline=True,
                                        ),
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
                                html.Div(id="selected-driver-label"),
                                dcc.Graph(id="track-graph"),
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


@app.callback(
    Output("event-track-graph", "figure"),
    Input("driver-dropdown", "value"),
)
def update_track_info_graph(selected_driver):
    if not selected_driver:
        selected_driver = drivers[:1]
        driver_laps = session.laps.pick_drivers(selected_driver)
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        lap = driver_laps.pick_fastest()
        tel = lap.get_telemetry()

        sector1_end_time = lap["Sector1Time"].total_seconds()
        sector2_end_time = sector1_end_time + lap["Sector2Time"].total_seconds()

        def assign_sector(time_seconds):
            if time_seconds <= sector1_end_time:
                return "Sector 1"
            elif time_seconds <= sector2_end_time:
                return "Sector 2"
            else:
                return "Sector 3"

        tel["TimeSeconds"] = tel["Time"].dt.total_seconds()
        tel["Sector"] = tel["TimeSeconds"].apply(assign_sector)

        fig = px.line(
            tel,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title=f"{year} {event} Track with Sectors",
        )

        fig.update_traces(line=dict(width=5))

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


track_info = dbc.Row(
    children=[
        dbc.Row(children=[html.H1(children="Track Info")]),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            [
                                html.Div(id="track-info-length"),
                                html.Div(id="track-info-name"),
                                html.Div(id="selected-driver-label"),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    children=[
                        html.Div(
                            [
                                dcc.Graph(id="event-track-graph"),
                            ]
                        )
                    ]
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("selected-driver-label", "children"), Input("driver-dropdown", "value")
)
def update_selected_driver_label(value):
    if not value:
        return dbc.Row(children=[html.Span("No driver selected")])
    elif len(value) == 1:
        return dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Span(
                            f"Inner Driver: {driver_number_fullname_map[value[0]]}"
                        )
                    ]
                )
            ]
        )
    else:
        return dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Span(
                            f"Inner Driver: {driver_number_fullname_map[value[0]]}"
                        )
                    ]
                ),
                dbc.Col(
                    children=[
                        html.Span(
                            f"Outer Driver: {driver_number_fullname_map[value[1]]}"
                        )
                    ]
                ),
            ]
        )


@app.callback(Output("driver-dropdown", "options"), Input("driver-dropdown", "value"))
def update_multi_options(value):
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


@app.callback(
    Output("track-graph", "figure"),
    Input("driver-dropdown", "value"),
    Input("telemetry-dropdown", "value"),
)
def update_graph(selected_driver, selected_telemetry):
    if not selected_telemetry:
        selected_telemetry = "Speed"

    if not selected_driver:
        selected_driver = drivers[:1]
        driver_laps = session.laps.pick_drivers(selected_driver)
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        lap = driver_laps.pick_fastest()
        tel = lap.get_telemetry()

        sector1_end_time = lap["Sector1Time"].total_seconds()
        sector2_end_time = sector1_end_time + lap["Sector2Time"].total_seconds()
        sector3_end_time = sector2_end_time + lap["Sector3Time"].total_seconds()

        def assign_sector(time_seconds):
            if time_seconds <= sector1_end_time:
                return "Sector 1"
            elif time_seconds <= sector2_end_time:
                return "Sector 2"
            else:
                return "Sector 3"

        tel["TimeSeconds"] = tel["Time"].dt.total_seconds()
        tel["Sector"] = tel["TimeSeconds"].apply(assign_sector)

        fig = px.line(
            tel,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title=f"{year} {event} Track with Sectors",
        )

        fig.update_traces(line=dict(width=5))

    elif len(selected_driver) == 1:
        driver_laps = session.laps.pick_drivers(selected_driver)
        if driver_laps.empty:
            return px.line(title=f"No data available for driver {selected_driver}")

        lap = driver_laps.pick_fastest()
        tel = lap.get_telemetry()

        sector1_end_time = lap["Sector1Time"].total_seconds()
        sector2_end_time = sector1_end_time + lap["Sector2Time"].total_seconds()
        sector3_end_time = sector2_end_time + lap["Sector3Time"].total_seconds()

        def assign_sector(time_seconds):
            if time_seconds <= sector1_end_time:
                return "Sector 1"
            elif time_seconds <= sector2_end_time:
                return "Sector 2"
            else:
                return "Sector 3"

        tel["TimeSeconds"] = tel["Time"].dt.total_seconds()
        tel["Sector"] = tel["TimeSeconds"].apply(assign_sector)
        scale_in = -250.0
        subj = tuple(tel[["X", "Y"]].itertuples(index=False, name=None))
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(subj, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        solution = pco.Execute(scale_in)

        df = pd.DataFrame(solution[0], columns=["X_prime", "Y_prime"])

        # for all points in df, compute min distance
        df["Original_Row"] = [
            np.argmin(np.linalg.norm(row - tel[["X", "Y"]], axis=1))
            for row in df.itertuples(index=False, name=None)
        ]
        df[selected_telemetry] = [
            tel.iloc[n][selected_telemetry] for n in df["Original_Row"]
        ]

        fig1 = px.line(
            tel,
            x="X",
            y="Y",
            color="Sector",
            line_group="Sector",
            title=f"{year} {event} Track with Sectors",
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
        driver_1_laps = session.laps.pick_drivers(selected_driver[:1])
        driver_2_laps = session.laps.pick_drivers(selected_driver[1:])

        lap_d1 = driver_1_laps.pick_fastest()
        lap_d2 = driver_2_laps.pick_fastest()
        tel_d1 = lap_d1.get_telemetry()
        tel_d2 = lap_d2.get_telemetry()

        sector1_end_time = lap_d1["Sector1Time"].total_seconds()
        sector2_end_time = sector1_end_time + lap_d1["Sector2Time"].total_seconds()
        sector3_end_time = sector2_end_time + lap_d1["Sector3Time"].total_seconds()

        def assign_sector(time_seconds):
            if time_seconds <= sector1_end_time:
                return "Sector 1"
            elif time_seconds <= sector2_end_time:
                return "Sector 2"
            else:
                return "Sector 3"

        tel_d1["TimeSeconds"] = tel_d1["Time"].dt.total_seconds()
        tel_d2["TimeSeconds"] = tel_d2["Time"].dt.total_seconds()
        tel_d1["Sector"] = tel_d1["TimeSeconds"].apply(assign_sector)
        tel_d2["Sector"] = tel_d2["TimeSeconds"].apply(assign_sector)

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
            title=f"{year} {event} Track with Sectors",
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


@app.callback(
    Output("event_name", "children"),
    Input("event_dropdown", "value"),
)
def display_select_event_name(event):
    preamble = "2024 Grand Prix"
    if event is None:
        return preamble
    return "2024" + f" {event['EventName']}"


@app.callback(
    Output("event_date", "children"),
    Input("event_dropdown", "value"),
)
def display_select_event_date(event):
    preamble = "Event Date:"
    if event is None:
        return preamble
    return preamble + f" {event['EventDate']}"


center = {"text_align": "center"}

picker = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(html.H3(id="event_name"), style=center),
                dbc.Col(html.H3(id="event_date"), style=center),
                dbc.Col(
                    html.Div(
                        children=[
                            html.H5(children=("Select Race")),
                            dcc.Dropdown(
                                id="event_dropdown",
                                options=[
                                    {"label": event["EventName"], "value": event}
                                    for event in events
                                ],
                            ),
                        ],
                    ),
                    style=center,
                ),
            ],
            align="center",
        ),
    ]
)

track_core_vis = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(children=[html.H5("Track Length", id="track_len")]),
                        dbc.Row(children=[html.H5("Number of Laps", id="num_laps")]),
                        dbc.Row(children=[html.H5("Something")]),
                    ],
                    width={"size": 2, "order": 1},
                ),
                dbc.Col(
                    html.Div(children=[html.H5("Track Vis")], id="track_vis"),
                    width={"size": 6, "order": 2},
                ),
                dbc.Col(
                    html.Div(children=[html.H5("Predicted Winners")]),
                    width={"size": 2, "order": 3},
                ),
                dbc.Col(
                    html.Div(children=[html.H5("Actual Winners")]),
                    width={"size": 2, "order": 4},
                ),
            ]
        )
    ]
)

# place_and_table_vis = html.Div(
#     children=[
#         dbc.Row(
#             children=[
#                 dbc.Column(
#                     children=[
#                         dbc.Row(children=[html.Div(id="first_place")]),
#                         dbc.Row(children=[html.Div(id="second_place")]),
#                         dbc.Row(children=[html.Div(id="third_place")]),
#                     ]
#                 ),
#                 dbc.Column(children=[html.H5("Data Table")]),
#             ]
#         ),
#     ]
# )

app.layout = dbc.Container(
    children=[
        # Tab 1
        navbar,
        picker,
        track_info,
        # track_core_vis,
        dbc.Row(
            """
            1-2: 
                1: driver, driver image, driver team, driver country flag, driver country, place
                2: driver, driver image, driver team, driver country flag, driver country, place
                3: driver, driver image, driver team, driver country flag, driver country, place
            3-4: 
                1: race standings data table
            """
        ),
        dbc.Stack(
            """
            Row 1: 
                1: pick driver names 
            Row 2-3: 
                1: lap times based on driver name 
            Row 4-5:
                1: position change
            """
        ),
        track_vis,
        dbc.Stack(
            """
            Row 1: Tyre strategy
            """
        ),
        # Tab 2
        dbc.Row(
            """
            1: Formula win
            4-5: 3 tabs
            """
        ),
        dbc.Stack(
            """
            Row 1: pick race, pick driver
            Row 2: Driver picture, Driver name, Driver country, driver team name, driver place, predicted place, actual place
            Row 3: lap times
            """
        ),
        # Tab 3
        dbc.Row(
            """
            1: Formula win
            4-5: 3 tabs
            """
        ),
        dbc.Row(
            """
            Col 1: Driver standings for season
            Col 2: Team standings for season
            """
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
