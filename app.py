import os

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

# Incorporate data
df = pd.read_csv("./data/product_changes.csv", index_col=0)
# Convert to % gain and round
df = df.sub([100, 100, 100], axis="columns").round(2)
df2 = pd.read_csv("./data/product_prices.csv", index_col=0)
df_income = pd.read_csv("./data/income.csv", index_col=0)
df_expenses = pd.read_csv("./data/expenses.csv", index_col=0)

# * Add bootstrap
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css"]
external_scripts = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"]
app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server
# App layout
app.layout = html.Div(
    className="container-fluid",
    children=[
        html.Div(
            className="row",
            children=[
                html.H4(
                    "Region expenses and income",
                    className="text-center",
                ),
                dcc.Dropdown(
                    id="dropdown-income",
                    options=list(df_income.columns),
                    value=df_income.columns[0],
                    clearable=False,
                ),
                html.Div(
                    className="col",
                    children=[
                        dcc.Graph(id="graph-expenses"),
                    ],
                ),
                html.Div(
                    className="col",
                    children=[
                        dcc.Graph(id="graph-income"),
                    ],
                ),
                html.Div(
                    className="col",
                    children=[
                        dcc.Graph(id="graph-income-expenses"),
                    ],
                ),
                html.Div(
                    className="row",
                    children=[
                        html.H4(
                            "Region expenses and income trend",
                            className="text-center",
                        ),
                        dcc.Dropdown(
                            id="dropdown-income-trend",
                            options=list(df_income.index),
                            value=df_income.index[0],
                            clearable=False,
                        ),
                        html.Div(
                            className="col",
                            children=[
                                dcc.Graph(id="graph-expenses-trend"),
                            ],
                        ),
                        html.Div(
                            className="col",
                            children=[
                                dcc.Graph(id="graph-income-trend"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.H4(
                    "Prices for products",
                    className="text-center",
                ),
                html.Div(
                    className="col-md-4",
                    children=[
                        html.Div(
                            className="table",
                            children=[
                                dash_table.DataTable(
                                    data=df2.reset_index().to_dict("records"),
                                    page_size=15,
                                    sort_action="native",
                                    sort_mode="multi",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="col",
                    children=[
                        dcc.Dropdown(
                            id="dropdown-prices",
                            options=list(df2.columns)[1:],
                            value=df.columns[1],
                            clearable=False,
                        ),
                        dcc.Graph(id="graph-prices"),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.H4(
                    "Price index in first quarter",
                    className="text-center",
                ),
                html.Div(
                    className="col-md-4",
                    children=[
                        html.Div(
                            className="table",
                            children=[
                                dash_table.DataTable(
                                    data=df.reset_index().to_dict("records"),
                                    page_size=15,
                                    sort_action="native",
                                    sort_mode="multi",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="col",
                    children=[
                        dcc.Dropdown(
                            id="dropdown",
                            options=list(df.index),
                            value=df.index[1],
                            clearable=False,
                        ),
                        dcc.Graph(id="graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("graph", "figure"), Input("dropdown", "value"))
def update_product_changes_chart(product):
    mask = df.filter(items=[product], axis=0)
    fig = px.bar(
        mask,
        y=["Jan", "Feb", "Mar"],
        barmode="group",
    )
    return fig


@app.callback(Output("graph-income", "figure"), Input("dropdown-income", "value"))
def update_region_income_graph(year):
    fig = px.bar(
        df_income[year].sort_values(),
        x=list(df_income.sort_values(by=[year]).index),
        y=year,
        barmode="group",
        title="Regions income by year",
    )
    return fig


@app.callback(Output("graph-income-expenses", "figure"), Input("dropdown-income", "value"))
def update_region_income_expenses_graph(year):
    fig = px.bar(
        df_income[year] - df_expenses[year],
        x=list(df_income.index),
        y=year,
        barmode="group",
        title="Regions income - expenses",
    )
    return fig


@app.callback(Output("graph-income-trend", "figure"), Input("dropdown-income-trend", "value"))
def update_region_income_trend(region):
    return px.line(
        df_income.loc[region],
        title="Income trend by region",
    )


@app.callback(Output("graph-expenses", "figure"), Input("dropdown-income", "value"))
def update_region_expenses_graph(year):
    fig = px.bar(
        df_expenses[year].sort_values(),
        x=list(df_expenses.sort_values(by=[year]).index),
        y=year,
        barmode="group",
        title="Regions Expenses by year",
    )
    return fig


@app.callback(Output("graph-expenses-trend", "figure"), Input("dropdown-income-trend", "value"))
def update_region_expenses_trend(region):
    return px.line(
        df_expenses.loc[region],
        title="Expenses trend by region",
    )


@app.callback(Output("graph-prices", "figure"), Input("dropdown-prices", "value"))
def update_scatter_chart(month):
    return px.scatter(
        df2[month],
        x=df2[month],
        size=month,
        size_max=60,
        color=month,
    )


if __name__ == "__main__":
    app.run(debug=os.environ["DEBUG"])
