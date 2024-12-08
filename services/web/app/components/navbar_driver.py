import dash_bootstrap_components as dbc
from dash import html
from ..components import driver_dropdown


def make_layout():
    return html.Div(
        id="navbar",
        children=[
            dbc.Navbar(
                dbc.Container(
                    children=[
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src="", height="30px")),
                                    dbc.Col(
                                        dbc.NavbarBrand(
                                            "FormulaWin",
                                            className="ms-2",
                                            style={"font-size": "1.75em"},
                                        )
                                    ),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                        dbc.Row(
                            [
                                dbc.Nav(
                                    [
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                "Grand Prix Summary",
                                                href="/",
                                            ),
                                            className="page-navigation",
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                "Driver Summary",
                                                href="/driver",
                                            ),
                                            className="page-navigation",
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                "Season Summary",
                                                href="/season",
                                            ),
                                            className="page-navigation",
                                        ),
                                    ],
                                    className="mx-auto",
                                )
                            ],
                        ),
                        dbc.Row(
                            [
                                driver_dropdown.make_layout(),
                            ]
                        ),
                    ],
                    fluid=True,
                ),
                className="custom-navbar",
            ),
        ],
    )
