import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback, html
from util import get_data


center = {"text_align": "center"}

event_picker = html.Div(
    children=[
        dbc.Row(
            children=[
                html.H5(children=("Select Grand Prix")),
                dcc.Dropdown(
                    id="RoundNumber_dropdown",
                    value=1,
                ),
            ],
            align="center",
        ),
    ],
)

interval = dcc.Interval(
    id="load_interval",
    n_intervals=0,
    max_intervals=0,  # <-- only run once
    interval=1,
)


def make_layout():
    return html.Div(
        id="navbar",
        children=[
            dbc.Row(
                [
                    interval,
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
                            dbc.Col(
                                children=[
                                    dbc.Row(children=[event_picker]),
                                ]
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


@callback(
    Output("RoundNumber_dropdown", "options"), Input("load_interval", "n_intervals")
)
def event_dropdown_update(n_intervals):
    with open("sql/events.sql") as f:
        query = f.read()
    df = get_data.get_data(query)
    df = df[df["Event"] < 21]
    df["EventName"] = df["Event"].astype(str) + ": " + df["EventName"]
    df = df.rename({"Event": "value", "EventName": "label"}, axis=1)
    df_list = df[["label", "value"]].to_dict(orient="records")
    return df_list
