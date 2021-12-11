import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output

pio.templates.default = "plotly_dark"
import dash_bootstrap_components as dbc
from app import app
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
HM_NHL = pd.read_pickle(DATA_PATH.joinpath("heat_map.pkl"))
NHL = pd.read_pickle(DATA_PATH.joinpath("NHL_edit.pkl"))

layout = dbc.Container(
    [
        html.Div(className="p-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.RangeSlider(
                            id="heat_map_year1",
                            min=int(HM_NHL.season.min()),
                            max=int(HM_NHL.season.max()),
                            marks=dict(
                                (int(x), str(x)) for x in sorted(HM_NHL.season.unique())
                            ),
                            step=1,
                            allowCross=False,
                            value=[int(HM_NHL.season.min()), int(HM_NHL.season.max())],
                            updatemode="drag",
                        ),
                        dcc.Dropdown(
                            id="HMteam1",
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
                        dcc.Graph(id="heatmap1"),
                    ],
                    width={"size": 6},
                ),
                dbc.Col(
                    [
                        dcc.RangeSlider(
                            id="heat_map_year2",
                            min=int(HM_NHL.season.min()),
                            max=int(HM_NHL.season.max()),
                            marks=dict(
                                (int(x), str(x)) for x in sorted(HM_NHL.season.unique())
                            ),
                            step=1,
                            allowCross=False,
                            value=[int(HM_NHL.season.min()), int(HM_NHL.season.max())],
                            updatemode="drag",
                        ),
                        dcc.Dropdown(
                            id="HMteam2",
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
                        dcc.Graph(id="heatmap2"),
                    ],
                    width={"size": 6},
                ),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("heatmap1", "figure"),
    [Input("heat_map_year1", "value"), Input("HMteam1", "value")],
)
def update_heatmap1(heat_map_year1, HMteam1):

    team_season = HM_NHL.loc[
        (
            (HM_NHL["team"] == HMteam1)
            & (HM_NHL["season"] >= heat_map_year1[0])
            & (HM_NHL["season"] <= heat_map_year1[1])
        ),
        :,
    ].set_index(["team", "season", "gameId"])
    fig = px.imshow(team_season.corr(), color_continuous_scale=px.colors.sequential.Jet)
    fig.update_xaxes(tickangle=25, tickfont=dict(size=10))
    return fig


@app.callback(
    Output("heatmap2", "figure"),
    [Input("heat_map_year2", "value"), Input("HMteam2", "value")],
)
def update_heatmap1(heat_map_year2, HMteam2):

    team_season = HM_NHL.loc[
        (
            (HM_NHL["team"] == HMteam2)
            & (HM_NHL["season"] >= heat_map_year2[0])
            & (HM_NHL["season"] <= heat_map_year2[1])
        ),
        :,
    ].set_index(["team", "season", "gameId"])
    fig = px.imshow(team_season.corr(), color_continuous_scale=px.colors.sequential.Jet)
    fig.update_xaxes(tickangle=25, tickfont=dict(size=10))
    return fig
