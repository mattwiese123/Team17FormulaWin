import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback, html
from util import get_data


def make_layout():
    return html.Div(
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
