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
        dbc.Row(
            children=[
                driver_standing.make_layout(),
            ]
        ),
    ]
)
