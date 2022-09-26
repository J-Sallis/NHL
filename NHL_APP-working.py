from distutils.log import debug
from pickle import TRUE
import pandas as pd
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from apps import table_playoff, heatmap_tab, hits_goals_tab, rebounds
from app import app
from app import server

app.layout = dbc.Container([
    dbc.Row([
    dbc.Col(html.H1("NHL Data Jesse Sallis " + str(pd.to_datetime('today').strftime("%m/%d/%Y")), className='text-center, mb-4'),width=12)
        ]),
    
    dbc.Tabs(
            [
                dbc.Tab(hits_goals_tab.layout,label="Hits/Goals by Team"),
                dbc.Tab(heatmap_tab.layout,label="Correlation Heatmap"),
                dbc.Tab(table_playoff.layout,label="Playoffs"),
                dbc.Tab(rebounds.layout,label="Rebounds"),
            ],
        ),
    
     html.Div(className="p-4"),
], fluid=True)

if __name__ == '__main__':
    app.run(debug=False)