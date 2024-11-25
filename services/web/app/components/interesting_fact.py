import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output
import pandas as pd
# from util import get_data


track_fun_facts = html.Div(id="track-fun-facts")


def make_layout():
    return html.Div(
        children=[
            # dbc.Row(children=[html.H1(children="Predicted vs Actual Top 3")]),
            dbc.Row(
                children=[
                    dbc.Col(children=[track_fun_facts]),
                ]
            ),
        ]
    )


@callback(
    Output("track-fun-facts", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def update_fun_fact(event):
    track_df = pd.read_csv("/usr/src/app/track_data.csv")
    col_list = [f"Fact{i}" for i in range(1, 6)]
    children = []

    children.append(
        html.H1(
            f'{track_df[track_df['Round']==event]['Grand Prix'].values[0]} Fun Facts'
        )
    )
    for i, col in enumerate(col_list):
        temp = dbc.Row(
            [
                html.H5(
                    [
                        f"Fun Fact {i+1}: {track_df[track_df['Round']==event][col].values[0]}"
                    ]
                )
            ]
        )
        children.append(temp)

    return children
