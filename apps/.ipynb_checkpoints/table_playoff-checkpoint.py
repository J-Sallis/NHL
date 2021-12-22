import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash_table import DataTable, FormatTemplate
from dash import html
import pathlib
from dash import dcc
from app import app
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
cup_df = pd.read_pickle(DATA_PATH.joinpath("playoffs_table.pkl"))
NHL_violin = pd.read_pickle(DATA_PATH.joinpath("NHL_violin.pkl"))

percentage = FormatTemplate.percentage(2)

layout = dbc.Container(
    [
        html.Div(className="p-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            id="table",
                            columns=[
                                dict(id="Season", name="Season"),
                                dict(id="Cup winner", name="Cup winner"),
                                dict(id="Goals per game", name="Goals per game"),
                                dict(
                                    id="Goals/game vs Reg Season",
                                    name="Goals/game vs Reg Season",
                                    type="numeric",
                                    format=percentage,
                                ),
                                dict(id="Hits per game", name="Hits per game"),
                                dict(
                                    id="Hits/game vs Reg Season",
                                    name="Hits/game vs Reg Season",
                                    type="numeric",
                                    format=percentage,
                                ),
                            ],
                            data=cup_df.to_dict("records"),
                            style_cell=dict(
                                textAlign="right",
                                color="black",
                                height="auto",
                                whitespace="normal",
                                minWidth="50px",
                                width="50px",
                                maxWidth="75px",
                            ),
                            style_header=dict(
                                backgroundColor="rgb(30, 30, 30)",
                                border="1px solid black",
                                color="white",
                                fontweight="bold",
                                textAlign="center",
                                whiteSpace="normal",
                            ),
                            style_data=dict(
                                backgroundColor="lavender", border="1px solid black"
                            ),
                            style_data_conditional=[
                                {
                                    "if": {
                                        "filter_query": "{Goals/game vs Reg Season} < 0",
                                        "column_id": "Goals/game vs Reg Season",
                                    },
                                    "fontWeight": "bold",
                                    "color": "tomato",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Goals/game vs Reg Season} > 0",
                                        "column_id": "Goals/game vs Reg Season",
                                    },
                                    "fontWeight": "bold",
                                    "color": "green",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Hits/game vs Reg Season} < 0",
                                        "column_id": "Hits/game vs Reg Season",
                                    },
                                    "fontWeight": "bold",
                                    "color": "tomato",
                                },
                                {
                                    "if": {
                                        "filter_query": "{Hits/game vs Reg Season} > 0",
                                        "column_id": "Hits/game vs Reg Season",
                                    },
                                    "fontWeight": "bold",
                                    "color": "green",
                                },
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "rgb(192,192,192)",
                                },
                            ],
                            sort_action="native",
                        )
                    ],
                    width={"size": 6}),
                dbc.Col([
    dcc.RadioItems(id='violin_CL',
        options=[
            {'label': 'Hits', 'value': 'hitsFor'},
            {'label': 'Goals', 'value': 'goalsFor'},
            
        ],
        value='hitsFor'
    ),dcc.Graph(id="violin")
],width={'size':6})
            ]
        ),
    ],
    fluid=True,
)
@app.callback(
    Output(component_id='violin', component_property='figure'),
    [Input(component_id='violin_CL', component_property='value')]
)
def update_graph(violin_CL):
    dff = NHL_violin
    fig = go.Figure()
    fig.add_trace(go.Violin(y=dff[violin_CL].loc[dff['playoffGame'] == 0],box_visible=True, line_color='pink', meanline_visible=True, fillcolor='darkred', opacity=0.5,x0='Regular'))
    fig.add_trace(go.Violin(y=dff[violin_CL].loc[dff['playoffGame'] == 1], box_visible=True, line_color='pink',meanline_visible=True, fillcolor='darkred', opacity=0.5, x0='Playoffs'))
    fig.update_layout(yaxis=dict(title=violin_CL,nticks = 12),xaxis=dict(title='Season'),title= violin_CL + ' Reg vs Playoffs',title_x=0.5,width=800,height=400,showlegend=False)
    return fig