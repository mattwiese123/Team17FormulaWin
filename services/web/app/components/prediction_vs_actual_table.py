from util import get_data
from dash import Input, Output, callback, dash_table


def make_layout():
    return (
        dash_table.DataTable(
            id="pred_table",
            style_as_list_view=True,
            style_cell={"padding": "2px", "textAlign": "center"},
            page_action="none",
            style_table={"height": "650px", "overflowY": "auto", "margin-top": "0.5em"},
            style_header={"backgroundColor": "white", "fontWeight": "bold"},
        ),
    )


@callback(
    Output("pred_table", "data"),
    Input("RoundNumber_dropdown", "value"),
)
def prediction_vs_actual_table(RoundNumber):
    with open("sql/get_pred.sql") as f:
        query = f.read()
    df = get_data.get_data(query.format(RoundNumber=RoundNumber))
    return df.to_dict("records")
