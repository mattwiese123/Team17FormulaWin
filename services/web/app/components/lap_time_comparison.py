import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, dcc
import pandas as pd

# from main import app
import plotly.express as px


def make_layout():
    return dcc.Loading(dcc.Graph(id="lapTime_fig"), type="circle")


@callback(
    Output("lapTime_fig", "figure"),
    Input("RoundNumber_dropdown", "value"),
    Input("driver_picker", "value"),
)
def lap_time_comparison(RoundNumber, Drivers):
    with open("sql/get_driver_compare.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    lapTime_fig = px.line(
        df[df["FullName"].isin(Drivers)],
        x="LapNumber",
        y="laptime",
        color="FullName",
        hover_name="FullName",
        hover_data=["LapNumber", "Position", "laptime"],
        title="<b>Lap Time</b>",
        render_mode="webgl",
    )
    lapTime_fig.update_traces(
        mode="markers+lines",
        # visible="legendonly"
    )
    lapTime_fig.update_yaxes(categoryorder="category descending")
    lapTime_fig.update_layout(
        plot_bgcolor="rgb(229,229,229)", xaxis=dict(rangemode="tozero")
    )
    return lapTime_fig
