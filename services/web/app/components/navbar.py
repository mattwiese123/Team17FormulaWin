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
                html.H5(children=("Track Rain Conditions")),
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
                                    dbc.Row(children=[driver_picker]),
                                    dbc.Row(children=[rain_picker]),
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


@callback(
    [Output("driver_picker", "options"), Output("driver_picker", "value")],
    Input("RoundNumber_dropdown", "value"),
)
def event_dropdown_update(event):
    with open("sql/get_event_drivers.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(EventNumber=event))
    df["label"] = df["ClassifiedPosition"] + ": " + df["FullName"]
    df = df.rename({"FullName": "value"}, axis=1)
    df_list = df[["label", "value"]].to_dict(orient="records")
    value = df.iloc[0]
    return df_list, value
