import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from util import get_data

event_track_graph = dcc.Graph(id="event-track-graph")

track_information = html.Div(id="track-information")


def make_layout():
    return html.Div(
        children=[
            dbc.Row(children=[html.H1(children="Track Info")]),
            dbc.Row(
                children=[
                    dbc.Col(children=[track_information]),
                    dbc.Col(children=[event_track_graph]),
                ]
            ),
        ]
    )


@callback(
    Output("track-information", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def update_event_info(event):
    track_df = pd.read_csv("/usr/src/app/track_data.csv")
    col_list = ["Length", "Total Laps", "Turns", "Type", "Direction"]
    children = []

    for col in col_list:
        temp = dbc.Row(
            [
                html.H5(
                    [
                        f"Track {col}: {track_df[track_df['Round']==event][col].values[0]}"
                    ]
                )
            ]
        )
        children.append(temp)

    return children


@callback(
    Output("event-track-graph", "figure"),
    Input("RoundNumber_dropdown", "value"),
)
def update_event_graph(event):
    def get_driver_tel_df(event: int):
        driver_string = "(" + ",".join([str(1)]) + ")"
        with open("sql/get_event_driver_telemetry.sql") as f:
            query = f.read()
        df = get_data.get_data(
            query.format(EventNumber=event, DriverNumbers=driver_string)
        )
        return df

    driver_laps = get_driver_tel_df(event)

    fig = px.scatter(
        driver_laps,
        x="X",
        y="Y",
        color="Sector",
        title="Track with Sectors",
    )

    fig.update_traces(line=dict(width=5))

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,1)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig
