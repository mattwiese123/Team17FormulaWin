import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, dcc
import pandas as pd

# from main import app
import plotly.express as px


def make_layout():
    return dcc.Graph(id="position_fig")


@callback(
    Output("position_fig", "figure"),
    Input("RoundNumber_dropdown", "value"),
    Input("driver_picker", "value"),
)
def position_comparison(RoundNumber, Drivers):
    with open("sql/get_driver_compare") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    position_fig = px.line(
        df[df["FullName"].isin(Drivers)],
        x="LapNumber",
        y="Position",
        color="FullName",
        hover_name="FullName",
        hover_data=["LapNumber", "Position", "laptime"],
    )
    position_fig.update_traces(
        mode="markers+lines",
        # visible="legendonly"
    )
    position_fig.update_layout(yaxis={"autorange": "reversed"})
    return position_fig

