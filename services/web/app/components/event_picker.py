import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback, html
from util import get_data


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
    return html.Div(children=[interval, event_picker])


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
