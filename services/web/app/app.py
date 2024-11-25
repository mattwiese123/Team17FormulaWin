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
    app.run_server(debug=True, dev_tools_silence_routes_logging=False)
