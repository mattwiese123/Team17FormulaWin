import dash
from dash import html, dcc

dash.register_page(__name__, path="/driver")


layout = html.Div(children=["driver"])
