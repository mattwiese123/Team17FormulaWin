import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
from util import get_data

event_track_graph = dcc.Loading(
    children=[dcc.Graph(id="event-track-graph")], type="circle"
)

track_information = dbc.Col(id="track-information")

track_fun_facts = html.Div(id="track-fun-facts")


def make_layout():
    return html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Row(children=[html.H3(children="Track Information")]),
                            dbc.Row(children=[track_information]),
                        ]
                    ),
                    dbc.Col(
                        children=[
                            dbc.Row(children=[event_track_graph]),
                        ]
                    ),
                ],
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Row(children=[track_fun_facts]),
                        ]
                    ),
                ]
            ),
        ]
    )


@callback(
    Output("track-information", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def update_event_info(event):
    with open("sql/get_track_metadata.sql") as f:
        query = f.read()
    track_df = get_data.get_data(query.format(EventNumber=event))
    columns_format = [dict(id="index", name=""), dict(id="0", name="")]
    return [
        dash_table.DataTable(
            markdown_options={"html": True},
            data=track_df.T.reset_index().to_dict(orient="records"),
            columns=columns_format,
            style_as_list_view=True,
            style_cell={"textAlign": "center"},
            style_header={"display": "none"},
        )
    ]


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
    children = []
    with open("sql/get_track_fun_facts.sql") as f:
        query = f.read()
    track_df = get_data.get_data(query.format(EventNumber=event))

    children.append(html.H3(f'{track_df['Grand Prix'].values[0]} Fun Facts'))
    ul = []
    for col in track_df.columns[1:]:
        temp = html.Li(f"{track_df[col].values[0]}")
        ul.append(temp)
    children.append(html.Ol(children=ul, className="fun-fact-list"))

    return children
