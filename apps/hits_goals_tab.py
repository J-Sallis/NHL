import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output
pio.templates.default = "plotly_dark"
import dash_bootstrap_components as dbc
import pathlib
from app import app
import numpy as np

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

NHL = pd.read_pickle(DATA_PATH.joinpath("NHL_edit.pkl"))

layout = dbc.Container(
    [
        html.Div(className="p-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="team",
                            options=[
                                {"label": x, "value": x}
                                for x in sorted(NHL.team.unique())
                            ],
                            clearable=True,
                            value="EDM",
                            style={"width": "40%"},
                            optionHeight=25,
                            multi=False,
                        ),
                        dcc.Graph(id="chart"),
                        html.Label(
                            "66% of NHL teams will fall within error bar range. Mean +/- 1 standard deviation"
                        ),
                    ],
                    width={"size": 7},
                    align="end",
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="pct-line-chart", figure={}),
                        html.Label(
                            "Points = Points/Total Potential Points, Hits/Goals = For/Against"
                        ),
                    ],
                    width={"size": 5},
                    align="end",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="chart2")], width={"size": 7}),
                dbc.Col(
                    [dcc.Graph(id="pct-line-chart2", figure={})],
                    width={"size": 5},
                    align="end",
                ),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output(component_id="chart", component_property="figure"),
    [Input(component_id="team", component_property="value")],
)
def update_graph(team):
    dff = NHL
    teams = dff.loc[dff["team"] == team, :]
    fig = go.Figure(
        data=[
            go.Bar(
                name="Goals For",
                x=teams.index,
                y=teams.goalsFor,
                marker_color="blue",
                error_y=dict(
                    type="data",
                    array=np.array(
                        (
                            (
                                dff.groupby(["season"])[["goalsFor"]].std()
                                + dff.groupby(["season"])[["goalsFor"]].mean()
                            )
                            .iloc[:, 0]
                            .sub(teams.goalsFor)
                        ).dropna()
                    ),
                    arrayminus=np.array(
                        (
                            teams.goalsFor.sub(
                                (
                                    dff.groupby(["season"])[["goalsFor"]].mean()
                                    - dff.groupby(["season"])[["goalsFor"]].std()
                                ).iloc[:, 0]
                            )
                        ).dropna()
                    ),
                    color="white",
                    thickness=3.0,
                    width=5,
                ),
            ),
            go.Bar(
                name="Goals Against",
                x=teams.index,
                y=teams.goalsAgainst,
                marker_color="red",
                error_y=dict(
                    type="data",
                    array=np.array(
                        (
                            (
                                dff.groupby(["season"])[["goalsAgainst"]].std()
                                + dff.groupby(["season"])[["goalsAgainst"]].mean()
                            )
                            .iloc[:, 0]
                            .sub(teams.goalsAgainst)
                        ).dropna()
                    ),
                    arrayminus=np.array(
                        (
                            teams.goalsAgainst.sub(
                                (
                                    dff.groupby(["season"])[["goalsAgainst"]].mean()
                                    - dff.groupby(["season"])[["goalsAgainst"]].std()
                                ).iloc[:, 0]
                            )
                        ).dropna()
                    ),
                    color="white",
                    thickness=3.0,
                    width=5,
                ),
            ),
        ]
    )
    fig.update_xaxes(dtick="Y1")
    fig.update_layout(
        barmode="group",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Goals"),
        title=(team + " Goals For/Against by Season"),
        title_x=0.5,
    )
    return fig


@app.callback(
    Output(component_id="chart2", component_property="figure"),
    [Input(component_id="team", component_property="value")],
)
def update_hits(team):
    dff = NHL
    teams = dff.loc[dff["team"] == team, :]
    hits = go.Figure(
        data=[
            go.Bar(
                name="Hits For",
                x=teams.index,
                y=teams.hitsFor,
                marker_color="blue",
                error_y=dict(
                    type="data",
                    array=np.array(
                        (
                            (
                                dff.groupby(["season"])[["hitsFor"]].std()
                                + dff.groupby(["season"])[["hitsFor"]].mean()
                            )
                            .iloc[:, 0]
                            .sub(teams.hitsFor)
                        ).dropna()
                    ),
                    arrayminus=np.array(
                        (
                            teams.hitsFor.sub(
                                (
                                    dff.groupby(["season"])[["hitsFor"]].mean()
                                    - dff.groupby(["season"])[["hitsFor"]].std()
                                ).iloc[:, 0]
                            )
                        ).dropna()
                    ),
                    color="white",
                    thickness=3.0,
                    width=5,
                ),
            ),
            go.Bar(
                name="Hits Against",
                x=teams.index,
                y=teams.hitsAgainst,
                marker_color="red",
                error_y=dict(
                    type="data",
                    array=np.array(
                        (
                            (
                                dff.groupby(["season"])[["hitsAgainst"]].std()
                                + dff.groupby(["season"])[["hitsAgainst"]].mean()
                            )
                            .iloc[:, 0]
                            .sub(teams.hitsAgainst)
                        ).dropna()
                    ),
                    arrayminus=np.array(
                        (
                            teams.hitsAgainst.sub(
                                (
                                    dff.groupby(["season"])[["hitsAgainst"]].mean()
                                    - dff.groupby(["season"])[["hitsAgainst"]].std()
                                ).iloc[:, 0]
                            )
                        ).dropna()
                    ),
                    color="white",
                    thickness=3.0,
                    width=5,
                ),
            ),
        ]
    )
    hits.update_xaxes(dtick="Y1")
    hits.update_layout(
        barmode="group",
        xaxis=dict(title="Season"),
        yaxis=dict(title="Hits"),
        title=(team + " Hits For/Against by Season"),
        title_x=0.5,
    )
    return hits


@app.callback(
    Output(component_id="pct-line-chart", component_property="figure"),
    [Input(component_id="team", component_property="value")],
)
def update_goals(team):
    dff = NHL
    teams = dff.loc[dff["team"] == team, :]
    fig = px.line(
        teams.sort_values(by=["season"], ascending=[True]),
        x=teams.index,
        y=["Goal_pct", "points"],
    )
    fig.update_xaxes(dtick="Y1")
    fig.update_layout(
        xaxis=dict(title="Season"),
        yaxis=dict(title="Percent"),
        title=(team + " Goals % by Season"),
        title_x=0.5,
    )
    return fig


@app.callback(
    Output(component_id="pct-line-chart2", component_property="figure"),
    [Input(component_id="team", component_property="value")],
)
def update_goals(team):
    dff = NHL
    teams = dff.loc[dff["team"] == team, :]
    fig = px.line(
        teams.sort_values(by=["season"], ascending=[True]),
        x=teams.index,
        y=["Hits_pct", "points"],
    )
    fig.update_xaxes(dtick="Y1")
    fig.update_layout(
        xaxis=dict(title="Season"),
        yaxis=dict(title="Percent"),
        title=(team + " Hits % by Season"),
        title_x=0.5,
    )
    return fig