import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output
from util import get_data

predicted_top_3 = html.Div(id="predicted-top-3-vis")
actual_top_3 = html.Div(id="actual-top-3-vis")


def make_layout():
    return html.Div(
        children=[
            # dbc.Row(children=[html.H1(children="Predicted vs Actual Top 3")]),
            dbc.Row(
                children=[
                    dbc.Col(children=[predicted_top_3]),
                    dbc.Col(children=[actual_top_3]),
                ]
            ),
        ]
    )


@callback(
    Output("predicted-top-3-vis", "children"),
    Output("actual-top-3-vis", "children"),
    Input("RoundNumber_dropdown", "value"),
)
def update_pred_v_t3_info(event):
    with open("sql/get_pred_v_actual.sql") as f:
        query = f.read()
    pred_df = get_data.get_data(query.format(EventNumber=event))
    actual_df = pred_df.copy()
    pred_df = pred_df.sort_values(by=["PredPos"]).head(3)
    actual_df = actual_df.sort_values(by=["ActualPosition"]).head(3)

    def make_top_3(df, position_col, title):
        # FullName, TeamName, PredPos, ActualPosition, Logo, HeadshotUrl
        driver_options = list()
        driver_options.append(html.H1(children=[title], style={"text-align": "center"}))
        for i, driver in enumerate(df.to_dict(orient="records")):
            driver_name = f"{driver['FullName']}"
            driver_position = (
                f"{driver[position_col]}" if driver[position_col] else f"{i+1}"
            )
            driver_label_list = html.Div(
                children=[
                    html.Div(
                        children=[
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            driver_position,
                                        ],
                                        style={
                                            "font-size": 32,
                                            "position": "absolute",
                                            "top": "1px",
                                            "left": "-50px",
                                            "color": "white",
                                            "text-shadow": "-1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black, 1px 1px 0 black",
                                        },
                                    ),
                                    html.Img(
                                        src=driver["HeadshotUrl"],
                                        style={
                                            "width": "120px",
                                            "height": "100px",
                                            "display": "block",
                                            "margin-left": "auto",
                                            "margin-right": "auto",
                                        },
                                    ),
                                ]
                            )
                        ],
                    ),
                    html.Span(
                        driver_name,
                        style={
                            "font-size": 24,
                            "color": "black",
                            "font-weight": "bold",
                            "padding-top": "-0.5em",
                        },
                    ),
                ],
                style={
                    "padding": 3,
                    "position": "relative",
                    "text-align": "center",
                },
            )

            driver_options.append(driver_label_list)
        return driver_options

    pred_col = make_top_3(pred_df, "PredPos", "Predicted Top 3")
    actual_col = make_top_3(actual_df, "ActualPosition", "Actual Top 3")

    return pred_col, actual_col
