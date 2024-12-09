import dash
from dash import html
import dash_bootstrap_components as dbc
from ..components import event_title
from ..components import weather
from ..components import lap_time_comparison
from ..components import position_comparison
from ..components import prediction_vs_actual_table
from ..components import prediction_vs_actual_top3
from ..components import track_visualization
from ..components import tyre_strategy
from ..components import track_perf
from ..components import driver_picker
from ..components import navbar_home

dash.register_page(__name__, path="/")


layout = dbc.Container(
    children=[
        dbc.Row(
            [
                navbar_home.make_layout(),
            ]
        ),
        html.Div(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            event_title.make_layout(),
                                        ),
                                        dbc.Row(weather.make_layout()),
                                        dbc.Row(
                                            [
                                                track_perf.make_layout(),
                                            ]
                                        ),
                                    ],
                                    className="vis-group",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(),
                                        dbc.Row(),
                                        dbc.Row(
                                            [prediction_vs_actual_top3.make_layout()]
                                        ),
                                        dbc.Row(
                                            children=[
                                                html.Div(
                                                    style={
                                                        "margin": "1em",
                                                        "padding": "1em",
                                                    }
                                                )
                                            ]
                                        ),
                                        dbc.Row(
                                            prediction_vs_actual_table.make_layout()
                                        ),
                                    ],
                                    className="vis-group",
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(driver_picker.make_layout()),
                                        dbc.Row(position_comparison.make_layout()),
                                        dbc.Row(lap_time_comparison.make_layout()),
                                        dbc.Row(tyre_strategy.make_layout()),
                                    ],
                                    className="vis-group",
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        track_visualization.make_layout(),
                                    ],
                                    className="vis-group",
                                )
                            ],
                        ),
                    ],
                    className="home-vis-container",
                ),
            ],
            className="home-vis-background",
        ),
    ],
    #     fluid=True,
    className="home-page-background",
)
