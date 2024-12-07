import dash_bootstrap_components as dbc
from dash import callback, dcc, html, Input, Output
from util import get_data


driver_dropdown = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H5(
                            children=["Select Driver"],
                            style={"textDecoration": "none"},
                            className="event-picker-header",
                        ),
                        dcc.Dropdown(
                            id="driver-dropdown",
                            value="Lewis Hamilton",  # Valor inicial
                            placeholder="Select a driver",
                        ),
                    ],
                    className="event-picker col-ms-md-auto",
                    style={"min-width": "300px", "color": "black"},
                ),
            ],
        ),
    ],
)

interval = dcc.Interval(
    id="load_interval_driver",
    n_intervals=0,
    max_intervals=0,  # <-- only run once
    interval=1,
)


def make_layout():
    return dbc.Col(children=[interval, driver_dropdown])


@callback(
    Output("driver-dropdown", "options"), Input("load_interval_driver", "n_intervals")
)
def driver_stats1_func(n_intervals):
    with open("sql/get_driver_stats2.sql") as f:
        query = f.read()
    res = get_data.get_data(query)
    return [
        {"label": f"{row["Position"]} {row["FullName"]}", "value": row["FullName"]}
        for row in res.to_dict(orient="records")
    ]
