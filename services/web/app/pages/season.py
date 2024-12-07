import dash
from dash import html

import dash_bootstrap_components as dbc
from ..components import team_standing

dash.register_page(__name__)


layout = dbc.Container(
    children=[
        # track_core_vis,
        dbc.Row(
            children=[
                team_standing.make_layout(),
            ]
        )
    ]
)
