import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback, html
from util import get_data


center = {"text_align": "center"}

event_picker = html.Div(
    children=[
        dbc.Row(
            children=[
                html.H5(children=("Select Event")),
                dcc.Dropdown(
                    id="RoundNumber_dropdown",
                    value=1,
                ),
            ],
            align="center",
        ),
    ],
)

driver_picker = html.Div(
    children=[
        dbc.Row(
            children=[
                html.H5(children=("Select Drivers")),
                dcc.Dropdown(
                    id="driver_picker",
                    options=[
                        "Alexander Albon",
                        "Carlos Sainz",
                        "Charles Leclerc",
                        "Fernando Alonso",
                        "Valtteri Bottas",
                    ],
                    value=["Alexander Albon", "Carlos Sainz"],
                    multi=True,
                ),
            ],
            align="center",
        ),
    ],
)

rain_picker = html.Div(
    children=[
        dbc.Row(
            children=[
                html.H5(children=("Track Rain")),
                dcc.Dropdown(
                    id="rain_dropdown",
                    options=[
                        {"label": "Rain", "value": "True"},
                        {"label": "No Rain", "value": "False"},
                    ],
                    value="True",
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
    return dbc.Row(
        [
            interval,
            dbc.NavbarSimple(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Row(children=[event_picker]),
                            dbc.Row(children=[driver_picker]),
                            dbc.Row(children=[rain_picker]),
                        ]
                    ),
                    # rain_picker,
                    dbc.NavItem(dbc.NavLink("Race Summary", href="/")),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More pages", header=True),
                            dbc.DropdownMenuItem("Event Summary", href="/"),
                            dbc.DropdownMenuItem("Driver Summary", href="/driver"),
                            dbc.DropdownMenuItem("Season Summary", href="/season"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                    ),
                ],
                brand="FormulaWin",
                brand_href="#",
                color="primary",
                dark=True,
                fluid=True,
                expand="xl",
            ),
        ]
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
