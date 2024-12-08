import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, html


def make_layout():
    return dbc.Col(
        children=[html.H3("Weather"), html.Pre(id="weather")],
        width={"size": "auto", "order": 1},
    )


@callback(Output("weather", "children"), Input("RoundNumber_dropdown", "value"))
def weather(RoundNumber):
    airtemp = 0
    humidity = 0
    pressure = 0
    rainfall = 0
    tracktemp = 0
    windspeed = 0
    with open("sql/get_event_weather.sql") as f:
        query = f.read()
    if RoundNumber <= 20:
        df = get_data.get_data(query.format(RoundNumber=RoundNumber))
        airtemp, humidity, pressure, rainfall, tracktemp, windspeed = list(
            df[
                [
                    "airtemp",
                    "humidity",
                    "pressure",
                    "rainfall",
                    "tracktemp",
                    "windspeed",
                ]
            ].values
        )[0]

    result = (
        "  air temp: "
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
        + "m/s  "
    )
    return result
