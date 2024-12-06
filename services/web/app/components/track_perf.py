import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from util import get_data

event_track_graph = dcc.Graph(id="event-track-graph")

track_information = html.Div(id="track-information")

track_fun_facts = html.Div(id="track-fun-facts")


def make_layout():
    return html.Div(
        children=[
            dbc.Row(children=[html.H4(children="Track Information")]),
            dbc.Row(html.Pre(children=[track_information])),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Row(children=[track_fun_facts]),
                        ]
                    ),
                    dbc.Col(
                        children=[
                            dbc.Row(children=[event_track_graph]),
                        ]
                    ),
                ],
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

    children.append("")
    for col in col_list:
        temp = f"  {col}: {track_df[track_df['Round']==event][col].values[0]}"
        children.append(temp)
    children.append("")

    return "  ".join(children)


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
        title=None,
    )

    fig.update_traces(line=dict(width=5))

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(229,229,229,1)",
        paper_bgcolor="rgba(229,229,229,0)",
        showlegend=False,
        margin=dict(l=5, r=5, t=5, b=5),
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig


@callback(
    Output("track-fun-facts", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def update_fun_fact(event):
    track_df = pd.read_csv("/usr/src/app/track_data.csv")
    col_list = [f"Fact{i}" for i in range(1, 6)]
    children = []

    children.append(
        html.H4(
            f'{track_df[track_df['Round']==event]['Grand Prix'].values[0]} Fun Facts'
        )
    )
    ul = []
    for col in col_list:
        temp = html.Li(f"{track_df[track_df['Round']==event][col].values[0]}")
        ul.append(temp)
    children.append(html.Ol(children=ul, className="fun-fact-list"))

    return children
