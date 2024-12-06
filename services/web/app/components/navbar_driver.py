import dash_bootstrap_components as dbc
from dash import html


def make_layout():
    return html.Div(
        id="navbar",
        children=[
            dbc.Row(
                [
                    dbc.NavbarSimple(
                        children=[
                            dbc.Nav(
                                dbc.DropdownMenu(
                                    children=[
                                        dbc.DropdownMenuItem("Dashboards", header=True),
                                        dbc.DropdownMenuItem(
                                            "Grand Prix Summary", href="/"
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Driver Summary", href="/driver"
                                        ),
                                        dbc.DropdownMenuItem(
                                            "Season Summary", href="/season"
                                        ),
                                    ],
                                    nav=True,
                                    in_navbar=True,
                                    label="Select Dashboard",
                                    direction="start",
                                ),
                            ),
                        ],
                        brand="FormulaWin",
                        brand_href="/",
                        color="primary",
                        dark=True,
                        fluid=True,
                        expand="xl",
                    ),
                ]
            )
        ],
    )
