import dash
from dash import Dash
import dash_bootstrap_components as dbc


# banner red : (225, 6, 0)
# font white : (255, 255, 255)

app = Dash(
    __package__,
    external_stylesheets=[
        # dbc.themes.JOURNAL,
        dbc.themes.BOOTSTRAP,
        "/usr/src/app/assets/style.css",
    ],
    use_pages=True,
)
server = app.server


app.layout = dbc.Container(
    children=[
        dash.page_container,
    ],
    #  fluid=True,
    className="page-background",
)

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_silence_routes_logging=False)
