import pandas as pd
from dash import dcc
from dash import html
import plotly.io as pio
from dash.dependencies import Input, Output
pio.templates.default = "plotly_dark"
import dash_bootstrap_components as dbc
import pathlib
import plotly.express as px
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
NHL_rebound = pd.read_pickle(DATA_PATH.joinpath("NHL_rebound.pkl"))

layout = dbc.Container([
    dcc.Dropdown(id='scatter_team',options=[
                                {"label": x, "value": x}
                                for x in sorted(NHL_rebound.team.unique())
                            ],
                            clearable=True,
                            value="EDM",style={"width": "50%"},
                            optionHeight=25,
                            multi=True),dcc.RangeSlider(
                            id="scat_year",
                            min=int(NHL_rebound.season.min()),
                            max=int(NHL_rebound.season.max()),
                            marks=dict(
                                (int(x), str(x)) for x in sorted(NHL_rebound.season.unique())
                            ),
                            step=1,
                            allowCross=False,
                            value=[int(NHL_rebound.season.min()), int(NHL_rebound.season.max())],
                            updatemode="drag",
                        ),
    
    dcc.Graph(id="scatter"), html.Label(
                            "Rebound shot attempt is defined as a shot within 3 seconds of rebound"
                        )])

@app.callback(
     Output(component_id='scatter', component_property='figure'),
     [Input(component_id='scatter_team', component_property='value'),Input(component_id='scat_year', component_property='value')])

def update_graph(scatter_team,scat_year):
    if type(scatter_team)!=str:
        dff = NHL_rebound.loc[((NHL_rebound['team'].isin(scatter_team)) & (NHL_rebound['season'] >= scat_year[0]) & (NHL_rebound['season'] <= scat_year[1])),:]
    else:
        dff = NHL_rebound.loc[((NHL_rebound['team'] == scatter_team) & (NHL_rebound['season'] >= scat_year[0]) & (NHL_rebound['season'] <= scat_year[1])),:]
    fig = px.scatter(dff, x='reboundsFor', y='reboundsAgainst',color='team',marginal_x="histogram", marginal_y="rug")
    fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 1,title='For'
    ),yaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 2, title='Against'
    ),title='Rebound Shot Attempts by Team',title_x=0.5,legend_title_text='Team'
)
    return fig
