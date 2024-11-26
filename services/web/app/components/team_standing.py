import plotly.graph_objects as go
from dash import callback, dcc, html, Input, Output
from util import get_data


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


team_points = team_points_func()
driver_points = driver_points_func()
driver_pointsA = driver_points[0:8]
driver_pointsB = driver_points[8:16]
driver_pointsC = driver_points[16:]


def create_team_table():
    # Crear la tabla
    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[
                    0.6,
                    0.3,
                    1.0,
                    0.2,
                    0.4,
                    1,
                ],  # Ajustar el ancho de las columnas
                header=dict(
                    values=[
                        "Position",
                        "",
                        "Team Name",
                        "-",
                        "Points",
                        "Points Label",
                    ],  # Encabezados de las columnas
                    fill_color="white",
                    font=dict(color="white", size=14),
                    align="center",
                ),
                cells=dict(
                    values=[
                        team_points["Position"],  # Columna Position
                        [""] * len(team_points),  # Columna vacía
                        team_points["TeamName"],  # Team Name
                        ["-"] * len(team_points),  # Símbolo "-"
                        team_points["Points"],  # Puntos
                        ["Points"]
                        * len(team_points),  # Etiqueta "Points" en todas las filas
                    ],
                    fill_color="white",
                    font=dict(color="black", size=24),
                    align=["center", "center", "left", "left", "center", "left"],
                    height=70,
                    line_color="white",  # Líneas separadoras
                ),
            )
        ]
    )

    imgy = [0.935, 0.835, 0.735, 0.635, 0.535, 0.430, 0.325, 0.225, 0.125, 0.025]

    # Agregar imágenes de logos
    for i, logo_url in enumerate(team_points["Logo"]):
        fig.add_layout_image(
            dict(
                source=logo_url,  # URL del logo
                x=0.14,  # Posición X de la imagen (ajustar según diseño)
                # y=1 - (i * 0.07),
                y=imgy[i],  # Posición Y basada en la fila
                xref="paper",  # Referencia a coordenadas del diseño
                yref="paper",
                sizex=0.1,  # Ancho de la imagen
                sizey=0.1,  # Alto de la imagen
                xanchor="left",  # Ancla izquierda
                yanchor="middle",  # Ancla centrada verticalmente
                layer="above",  # Colocar sobre otros elementos
            )
        )

    # Configurar diseño
    fig.update_layout(
        width=800,
        height=800,
        margin=dict(l=10, r=10, t=100, b=10),
        title=dict(
            text="Team",
            font=dict(
                family="Comic Sans MS",  # Fuente Comic Sans MS
                size=50,  # Tamaño del texto
                color="black",  # Color del texto
            ),
            x=0.5,  # Centrar el título horizontalmente
            xanchor="center",
            yanchor="top",
        ),
    )

    # Mostrar la figura
    # fig.show()

    return fig


def create_driver_table(datat):
    # Crear la tabla
    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[0.6, 0.3, 1.1, 0.2, 0.4, 1],
                header=dict(
                    values=["Position", "", "FullName", "-", "Points", "Points Label"],
                    fill_color="white",
                    font=dict(color="white", size=14),
                    align="center",
                ),
                cells=dict(
                    values=[
                        datat["Position"],
                        [""] * len(datat),
                        datat["FullName"],
                        ["-"] * len(datat),
                        datat["Points"],
                        ["Points"] * len(datat),
                    ],
                    fill_color="white",
                    font=dict(color="black", size=24),
                    align=["center", "center", "left", "left", "center", "left"],
                    height=70,
                    line_color="white",
                ),
            )
        ]
    )

    if len(datat) == 8:
        imgy = [0.935, 0.83, 0.73, 0.63, 0.53, 0.43, 0.33, 0.23]

    else:
        imgy = [0.935, 0.83, 0.73, 0.63, 0.53, 0.43, 0.33]

    # Agregar imágenes de logos
    for i, logo_url in enumerate(datat["Photo"]):
        fig.add_layout_image(
            dict(
                source=logo_url,
                x=0.14,
                y=imgy[i],
                xref="paper",
                yref="paper",
                sizex=0.08,
                sizey=0.08,
                xanchor="left",
                yanchor="middle",
                layer="above",
            )
        )

    # Configurar diseño
    fig.update_layout(
        width=800,
        height=800,
        margin=dict(l=10, r=10, t=100, b=10),
        title=dict(
            text="Driver",
            font=dict(family="Comic Sans MS", size=50, color="black"),
            x=0.5,
            xanchor="center",
            yanchor="top",
        ),
    )

    return fig


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
                            dcc.Graph(
                                figure=create_team_table(), style={"height": "100%"}
                            ),
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                            "margin-top": "50px",
                        },
                    ),
                    # Contenedor de conductores
                    html.Div(
                        [
                            # Menú desplegable
                            html.Div(
                                dcc.Dropdown(
                                    id="driver-dropdown",
                                    options=[
                                        {"label": "Driver Page 1", "value": "A"},
                                        {"label": "Driver Page 2", "value": "B"},
                                        {"label": "Driver Page 3", "value": "C"},
                                    ],
                                    value="A",
                                    style={
                                        "text-align": "center",
                                        "border-radius": "5px",
                                        "width": "50%",
                                        "margin": "auto",
                                        "font-size": "16px",
                                    },
                                ),
                                style={
                                    "text-align": "center",
                                    "margin-bottom": "20px",
                                },  # Contenedor con estilo general
                            ),
                            # Gráfico de conductores
                            dcc.Graph(id="driver-table", style={"height": "90%"}),
                        ],
                        style={
                            "width": "50%",
                            "display": "inline-block",
                            "vertical-align": "top",
                        },
                    ),
                ]
            ),
        ]
    )


# Callback para actualizar la tabla de drivers
@callback(Output("driver-table", "figure"), [Input("driver-dropdown", "value")])
def update_driver_table(selected_table):
    if selected_table == "A":
        return create_driver_table(driver_pointsA)
    elif selected_table == "B":
        return create_driver_table(driver_pointsB)
    elif selected_table == "C":
        return create_driver_table(driver_pointsC)
