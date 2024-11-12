import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from .components import driver_career
from .components import driver_perf_this_season
from .components import driver_profile
from .components import driver_standing
from .components import event_title_and_weather
from .components import interesting_fact
from .components import lap_time_comparison
from .components import navbar
from .components import position_comparison
from .components import prediction_vs_actual_table
from .components import prediction_vs_actual_top3
from .components import team_standing
from .components import track_info
from .components import track_perf
from .components import tyre_strategy

info_df = pd.read_csv("/usr/src/app/data/intermediate_tables/2019/8/info_2019_8.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME])
server = app.server


events = {"event1": {"country": "Bahrain", "date": "2024-10-10"}}


@app.callback(
    Output("event_name", "children"),
    Input("event_dropdown", "value"),
)
def display_select_event_name(event):
    preamble = "2024 Grand Prix"
    if event is None:
        return preamble
    return preamble + f" {event['country']}"


@app.callback(
    Output("event_date", "children"),
    Input("event_dropdown", "value"),
)
def display_select_event_date(event):
    preamble = "Event Date:"
    if event is None:
        return preamble
    return preamble + f" {event['date']}"


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
                                    {"label": k, "value": v} for k, v in events.items()
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
        track_core_vis,
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
        dbc.Stack(
            """
            Row 1: pick up to 2 driver names
            Row 2: 
                Col1: heatmap of lap times for driver 1
                Col2: track graph
                Col3: heatmap of lap times for driver 2
            """
        ),
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
