import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, html
import pandas as pd
# from main import app


def make_layout():
    return dbc.Col(
        children=[
            html.Pre(html.H1(id="event_name")),
            html.Pre(html.H3(id="event_date")),
        ],
        width={"size": "auto", "order": 1},
    )


@callback(
    Output("event_name", "children"),
    Output("event_date", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def event_title(RoundNumber):
    with open("sql/get_event_weather.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    event_name = df["EventName"][0]
    location = df["Location"][0]
    date = df["EventDate"][0]
    result_title = event_name + " (" + location + ")"
    result_date = "date: " + date.strftime("%Y-%m-%d")
    return result_title, result_date
