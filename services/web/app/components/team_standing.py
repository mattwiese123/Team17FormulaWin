import plotly.graph_objects as go
from dash import callback, dcc, html, Input, Output, dash_table
from util import get_data
import dash_bootstrap_components as dbc


def team_points_func():
    with open("sql/get_team_points.sql") as f:
        query = f.read()
    team_points = get_data.get_data(query)

    return team_points


def driver_points_func():
    with open("sql/get_driver_points.sql") as f:
        query = f.read()
    driver_points = get_data.get_data(query)
    return driver_points


def create_team_table(team_points):
    # Crear la tabla
    col_map = {
        "Logo": dict(
            id="Logo",
            name="",
            presentation="markdown",
        ),
        "Position": dict(id="Position", name="", presentation="markdown"),
    }
    columns_format = [
        dict(id=col, name=col) if col not in ("Logo", "Position") else col_map[col]
        for col in team_points.columns
    ]
    table = dash_table.DataTable(
        markdown_options={"html": True},
        data=team_points.to_dict(orient="records"),
        columns=columns_format,
        style_as_list_view=True,
        style_cell={"text-align": "left"},
        style_data_conditional=[
            {"if": {"column_id": c}, "fontSize": "20px", "font-weight": "bold"}
            for c in ("Position")
        ],
    )
    return table


def create_driver_table(datat):
    # Crear la tabla
    col_map = {
        "Photo": dict(id="Photo", name="", presentation="markdown"),
        "Position": dict(id="Position", name="", presentation="markdown"),
    }
    columns_format = [
        dict(id=col, name=col) if col not in ("Photo", "Position") else col_map[col]
        for col in datat.columns
    ]
    return dash_table.DataTable(
        markdown_options={"html": True},
        data=datat.to_dict(orient="records"),
        columns=columns_format,
        style_as_list_view=True,
        style_cell_conditional=[
            {"if": {"column_id": c}, "textAlign": "center"} for c in datat.columns
        ],
    )


team_points = team_points_func()
driver_points = driver_points_func()

team_fig_table = create_team_table(team_points)
driver_fig_table = create_driver_table(driver_points)


def make_layout():
    return html.Div(
        [
            # Título general
            html.H1(
                "2024 F1 Season Standings",
                style={
                    "text-align": "left",  # Alineado a la izquierda
                    "margin-bottom": "20px",
                    "color": "black",
                    "font-size": "50px",
                },
            ),
            # Contenedor general
            html.Div(
                [
                    # Tabla de equipos
                    html.Div(
                        [
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        html.H1(
                                            children=["Teams"],
                                            style={"text-align": "left"},
                                        ),
                                    ),
                                ]
                            ),
                            team_fig_table,
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "35px",
                        },
                    ),
                    # Contenedor de conductores
                    html.Div(
                        [
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        html.H1(
                                            children=["Drivers"],
                                            style={"text-align": "left"},
                                        ),
                                    ),
                                ]
                            ),
                            driver_fig_table,
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "35px",
                        },
                    ),
                ]
            ),
        ]
    )
