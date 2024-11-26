import dash
from dash import html, dcc, callback, Input, Output
from util import get_data
import dash_bootstrap_components as dbc
from ..components import event_title
from ..components import weather
from ..components import lap_time_comparison
from ..components import position_comparison
from ..components import prediction_vs_actual_table
from ..components import prediction_vs_actual_top3
from ..components import interesting_fact
from ..components import track_visualization
from ..components import tyre_strategy
from ..components import track_perf

dash.register_page(__name__, path="/")

driver_picker = html.Div(
    children=[
        dbc.Row(
            children=[
                html.H5(children=("Select Drivers")),
                dcc.Dropdown(
                    id="driver_picker",
                    options=[
                        "Alexander Albon",
                        "Carlos Sainz",
                        "Charles Leclerc",
                        "Fernando Alonso",
                        "Valtteri Bottas",
                    ],
                    value=["Alexander Albon", "Carlos Sainz"],
                    multi=True,
                ),
            ],
            align="center",
        ),
    ],
)

layout = dbc.Container(
    children=[
        # track_core_vis,
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            event_title.make_layout(),
                        ),
                        dbc.Row(weather.make_layout()),
                        dbc.Row(
                            [
                                dbc.Col([track_perf.make_layout()]),
                                dbc.Col([prediction_vs_actual_top3.make_layout()]),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(interesting_fact.make_layout()),
                                dbc.Col(prediction_vs_actual_table.make_layout()),
                            ]
                        ),
                        dbc.Row(position_comparison.make_layout()),
                        dbc.Row(driver_picker),
                        dbc.Row(lap_time_comparison.make_layout()),
                        dbc.Row(tyre_strategy.make_layout()),
                        dbc.Row(
                            track_visualization.make_layout(),
                        ),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
)


@callback(
    [Output("driver_picker", "options"), Output("driver_picker", "value")],
    Input("RoundNumber_dropdown", "value"),
)
def event_dropdown_update(event):
    with open("sql/get_event_drivers.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(EventNumber=event))
    df["label"] = df["ClassifiedPosition"] + ": " + df["FullName"]
    df = df.rename({"FullName": "value"}, axis=1)
    df_list = df[["label", "value"]].to_dict(orient="records")
    value = df.iloc[0]
    return df_list, value
