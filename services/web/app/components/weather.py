import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, html
import pandas as pd
# from main import app


def make_layout():
    return dbc.Col(html.Pre(id="weather"), width={"size": "auto", "order": 1})


@callback(Output("weather", "children"), Input("RoundNumber_dropdown", "value"))
def weather(RoundNumber):
    with open("sql/get_event_weather") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    airtemp, humidity, pressure, rainfall, tracktemp, windspeed = list(
        df[
            ["airtemp", "humidity", "pressure", "rainfall", "tracktemp", "windspeed"]
        ].values
    )[0]
    result = (
        "air temp: "
        + str(int(airtemp))
        + "°C    humidity: "
        + str(int(humidity))
        + "%    pressure: "
        + str(int(pressure))
        + "mbar    rainfall: "
        + str(rainfall)
        + "    track temp: "
        + str(int(tracktemp))
        + "°C    wind speed: "
        + str(int(windspeed))
        + "m/s"
    )
    return result
