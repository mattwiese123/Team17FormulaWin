import plotly.graph_objects as go
from dash import callback, dcc, html, Input, Output, no_update
from util import get_data


def driver_stats1_func():
    with open("sql/get_driver_stats1.sql") as f:
        query = f.read()
    res = get_data.get_data(query)

    return res


def driver_stats2_func():
    with open("sql/get_driver_stats2.sql") as f:
        query = f.read()
    driver_stats2 = get_data.get_data(query)

    return driver_stats2


def driver_stats3_func():
    with open("sql/get_driver_stats3.sql") as f:
        query = f.read()
    driver_stats3 = get_data.get_data(query)

    return driver_stats3


driver_stats1 = driver_stats1_func()
driver_stats2 = driver_stats2_func()
driver_stats3 = driver_stats3_func()


def make_layout():
    return html.Div(
        [
            dcc.Graph(
                id="driver-stats-graph-2",
            ),
            dcc.Graph(
                id="driver-stats-table",
            ),
        ]
    )


# Callback para actualizar el segundo gráfico
@callback(Output("driver-stats-graph-2", "figure"), [Input("driver-dropdown", "value")])
def update_graph_2(selected_driver):
    if not selected_driver:
        return no_update
    else:
        driver_data = driver_stats2[driver_stats2["FullName"] == selected_driver].iloc[
            0
        ]
        fig = go.Figure(
            data=[
                go.Table(
                    columnorder=[2, 3, 4, 5, 6, 7],
                    columnwidth=[0.8, 1, 1, 0.6, 1, 0.6],
                    header=dict(
                        values=[
                            "Driver",
                            "Nationality",
                            "Team",
                            "Current Rank",
                            "Championships",
                            "Wins",
                        ],
                        fill_color=[
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                        ],
                        font=dict(
                            color=[
                                "black",
                                "black",
                                "black",
                                "black",
                                "black",
                                "black",
                            ],
                            size=[18, 18, 18, 18, 18, 18],
                        ),
                        align=[
                            "center",
                            "center",
                            "center",
                            "center",
                            "center",
                            "center",
                        ],
                        height=30,
                        line_color=[
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                        ],
                    ),
                    cells=dict(
                        values=[
                            [driver_data["FullName"]],
                            [driver_data["Country"]],
                            [driver_data["Team"]],
                            [driver_data["Position"]],
                            [driver_data["Championships"]],
                            [driver_data["Wins"]],
                        ],
                        fill_color=[
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                        ],
                        font=dict(
                            color=[
                                "black",
                                "black",
                                "black",
                                "black",
                                "black",
                                "black",
                            ],
                            size=28,
                        ),
                        align=[
                            "center",
                            "center",
                            "center",
                            "center",
                            "center",
                            "center",
                        ],
                        height=40,
                        line_color=[
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                            "white",
                        ],
                    ),
                )
            ]
        )
        fig.add_layout_image(
            source=driver_data["Photo"],
            x=-0.13,
            y=0.10,  # Ajustar posición de la imagen
            xref="paper",
            yref="paper",
            sizex=1.5,
            sizey=1.5,
            xanchor="left",
            yanchor="bottom",
        )
        fig.update_layout(
            margin=dict(l=250, r=10, t=110, b=10),
            # width=1500,
            height=250,
            paper_bgcolor="white",
        )
        return fig


# Callback para actualizar el tercer gráfico
@callback(Output("driver-stats-table", "figure"), [Input("driver-dropdown", "value")])
def update_table(selected_driver):
    driver_data = driver_stats3[driver_stats3["FullName"] == selected_driver].drop(
        columns=["FullName"]
    )
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["<b>" + col + "</b>" for col in driver_data.columns],
                    fill_color="black",
                    font=dict(color="white", size=14),
                    align="center",
                ),
                cells=dict(
                    values=[driver_data[col].values for col in driver_data.columns],
                    fill_color="white",
                    font=dict(color="black", size=12),
                    align="center",
                ),
            )
        ]
    )
    fig.update_layout(paper_bgcolor="white")  # , width=1600, height=400)
    return fig
