import dash
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
