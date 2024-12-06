import dash
from dash import html

import dash_bootstrap_components as dbc
from ..components import team_standing
from ..components import navbar_season

dash.register_page(__name__)


layout = dbc.Container(
    children=[
        dbc.Row(
            [
                navbar_season.make_layout(),
            ]
        ),
        dbc.Row(
            children=[
                team_standing.make_layout(),
            ]
        ),
    ]
)
