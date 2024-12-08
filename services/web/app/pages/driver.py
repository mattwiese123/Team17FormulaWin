import dash
from dash import html
import dash_bootstrap_components as dbc
from ..components import driver_standing
from ..components import navbar_driver

dash.register_page(__name__)


layout = dbc.Container(
    children=[
        dbc.Row(
            [
                navbar_driver.make_layout(),
            ]
        ),
        html.Div(
            children=[
                dbc.Container(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            [
                                                html.H1(
                                                    "2024 F1 Driver Statistics",
                                                    style={
                                                        "textAlign": "left",
                                                    },
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            children=[
                                                driver_standing.make_layout(),
                                            ],
                                            className="vis-group",
                                        )
                                    ]
                                ),
                            ]
                        )
                    ],
                    className="home-vis-container",
                )
            ],
            className="home-vis-background",
        ),
    ],
    className="home-page-background",
)
