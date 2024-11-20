import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, dcc
import pandas as pd
from main import app
import plotly.express as px
import plotly.graph_objects as go


def make_layout():
    return dcc.Graph(id="tyre_fig")


@callback(
    Output('tyre_fig', 'figure'),
    Input('RoundNumber_dropdown', 'value'),
    Input('driver_picker', 'value')
)
def tyre_strategy(RoundNumber, Drivers):
    with open('sql/get_driver_compare') as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    df['Lap'] = 1
    tyre_fig = px.bar(df[df['FullName'].isin(Drivers)],
                           x="Lap", y="FullName",
                           color='Compound',
                           hover_name="FullName",
                           hover_data=["LapNumber", "Position", "laptime", 'Compound', 'TyreLife'],
                           orientation = 'h')

    return tyre_fig