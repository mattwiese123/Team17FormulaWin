import dash_bootstrap_components as dbc
from util import get_data
from dash import Input, Output, callback, dash_table
import pandas as pd

# from main import app
import plotly.express as px


def make_layout():
    return (
        dash_table.DataTable(
            id="pred_table",
            style_as_list_view=True,
            style_cell={"padding": "2px"},
            page_action="none",
            style_table={"height": "600px", "overflowY": "auto"},
            style_header={"backgroundColor": "white", "fontWeight": "bold"},
        ),
    )


@callback(
    Output("pred_table", "data"),
    Input("RoundNumber_dropdown", "value"),
)
def prediction_vs_actual_table(RoundNumber, has_rain):
    with open("sql/get_pred.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    if RoundNumber == 21:
        if has_rain == "True":
            df = df.loc[df["has_rain_R"] == True]
        else:
            df = df.loc[df["has_rain_R"] == False]
    pred_table = df[
        [
            "FullName",
            "TeamName",
            "EventFormat",
            "Position_Q",
            "CleanPredictedPosition",
            "ActualPosition",
        ]
    ]
    pred_table.columns = [
        "FullName",
        "TeamName",
        "EventFormat",
        "GridPosition",
        "PredictedPosition",
        "ActualPosition",
    ]
    return pred_table.sort_values(by=["ActualPosition", "PredictedPosition"]).to_dict(
        "records"
    )
