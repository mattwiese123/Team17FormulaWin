import plotly.graph_objects as go
from dash import callback, dcc, html, Input, Output, no_update, dash_table
from util import get_data
import dash_bootstrap_components as dbc


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
            dbc.Row(
                id="driver-stats-table",
            ),
        ],
        style={"marin": "0.15em", "padding": "0.15em"},
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
@callback(Output("driver-stats-table", "children"), [Input("driver-dropdown", "value")])
def update_table(selected_driver):
    driver_data = driver_stats3[driver_stats3["FullName"] == selected_driver].drop(
        columns=["FullName"]
    )
    return dash_table.DataTable(
        markdown_options={"html": True},
        data=driver_data.to_dict(orient="records"),
        # columns=columns_format,
        style_as_list_view=True,
        style_table={
            "margin": "0.25em",
            "padding": "0.25em",
        },
        style_header={
            "background-color": "black",
            "color": "white",
            "padding": "0.15em",
            "margin": "0.15em",
            "text-align": "left",
        },
        style_cell_conditional=[
            {"if": {"column_id": c}, "textAlign": "left"} for c in driver_data.columns
        ],
    )
