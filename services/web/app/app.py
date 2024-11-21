import dash
from dash import Dash
import dash_bootstrap_components as dbc


from .components import navbar

app = Dash(
    __package__,
    external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME],
    use_pages=True,
)
server = app.server


# track_core_vis = html.Div(
#     children=[
#         dbc.Row(
#             children=[
#                 dbc.Col(
#                     children=[
#                         dbc.Row(children=[html.H5("Track Length", id="track_len")]),
#                         dbc.Row(children=[html.H5("Number of Laps", id="num_laps")]),
#                         dbc.Row(children=[html.H5("Something")]),
#                     ],
#                     width={"size": 2, "order": 1},
#                 ),
#                 dbc.Col(
#                     html.Div(children=[html.H5("Track Vis")], id="track_vis"),
#                     width={"size": 6, "order": 2},
#                 ),
#                 dbc.Col(
#                     html.Div(children=[html.H5("Predicted Winners")]),
#                     width={"size": 2, "order": 3},
#                 ),
#                 dbc.Col(
#                     html.Div(children=[html.H5("Actual Winners")]),
#                     width={"size": 2, "order": 4},
#                 ),
#             ]
#         )
#     ]
# )

# place_and_table_vis = html.Div(
#     children=[
#         dbc.Row(
#             children=[
#                 dbc.Column(
#                     children=[
#                         dbc.Row(children=[html.Div(id="first_place")]),
#                         dbc.Row(children=[html.Div(id="second_place")]),
#                         dbc.Row(children=[html.Div(id="third_place")]),
#                     ]
#                 ),
#                 dbc.Column(children=[html.H5("Data Table")]),
#             ]
#         ),
#     ]
# )


app.layout = dbc.Container(
    children=[
        # navbar
        dbc.Row(
            [
                navbar.make_layout(),
            ]
        ),
        dash.page_container,
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
