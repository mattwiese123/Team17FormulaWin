import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, html
import pandas as pd
# from main import app


def make_layout():
    return dbc.Col(
        html.Pre(html.H3(id="event_name")), width={"size": "auto", "order": 1}
    )


@callback(Output("event_name", "children"), Input("RoundNumber_dropdown", "value"))
def event_title(RoundNumber):
    with open("sql/get_event_weather.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    event_name = df["EventName"][0]
    location = df["Location"][0]
    date = df["EventDate"][0]
    result = (
        event_name
        + " ("
        + location
        + ")"
        + "                date: "
        + date.strftime("%Y-%m-%d")
    )
    return result
