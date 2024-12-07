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
        "Logo": dict(id="Logo", name="", presentation="markdown"),
        "Position": dict(id="Position", name=""),
    }
    columns_format = [
        dict(id=col, name=col) if col not in ("Logo", "Position") else col_map[col]
        for col in team_points.columns
    ]
    return dash_table.DataTable(
        markdown_options={"html": True},
        data=team_points.to_dict(orient="records"),
        columns=columns_format,
        style_as_list_view=True,
        style_cell_conditional=[
            {"if": {"column_id": c}, "textAlign": "center"} for c in team_points.columns
        ],
    )


def create_driver_table(datat):
    # Crear la tabla
    col_map = {
        "Photo": dict(id="Photo", name="", presentation="markdown"),
        "Position": dict(id="Position", name=""),
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
                "F1 Standings",
                style={
                    "text-align": "center",  # Alineado a la izquierda
                    "font-family": "Arial, sans-serif",
                    "margin-bottom": "20px",
                    "margin-left": "-80px",  # Separación desde el borde izquierdo
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
                                    dbc.Col(),
                                    dbc.Col(
                                        html.H1(
                                            children=["Teams"],
                                        ),
                                    ),
                                    dbc.Col(),
                                ]
                            ),
                            team_fig_table,
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "25px",
                        },
                    ),
                    # Contenedor de conductores
                    html.Div(
                        [
                            dbc.Row(
                                children=[
                                    dbc.Col(),
                                    dbc.Col(
                                        html.H1(
                                            children=["Drivers"],
                                        ),
                                    ),
                                    dbc.Col(),
                                ]
                            ),
                            driver_fig_table,
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "padding": "25px",
                        },
                    ),
                ]
            ),
        ]
    )
