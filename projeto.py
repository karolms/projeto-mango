import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#banco de dados https://www.kaggle.com/usgs/pesticide-use?select=2015.csv


pesticide_2015 = pd.read_csv('2015.csv')
info_states = pd.read_csv('dictionary.csv')

pesticide = pesticide_2015.merge(info_states, how='left', on=['STATE_CODE', 'COUNTY_CODE'])


#tentativa de agrupar os condados e somar a quantidade de pesticidas
#pesticide_grouped = pesticide.groupby(['COMPOUND','STATE'])['HIGH_ESTIMATE'].sum().reset_index()

app = dash.Dash()

county_graph = html.Div(children=[
    html.H1(children= 'Pesticidas em 2015 por condado'),
    dcc.Dropdown(id = 'pesticide-county-dropdown',
                options = [{'label': i, 'value': i}
                            for i in pesticide['COMPOUND'].unique()],
                value='2,4-D'),
    dcc.Graph(id='pesticide-county-graph')
])

state_graph = html.Div(children=[
    html.H1(children= 'Pesticidas em 2015 por estado'),
    dcc.Dropdown(id = 'pesticide-state-dropdown',
                options = [{'label': i, 'value': i}
                            for i in pesticide['COMPOUND'].unique()],
                value='2,4-D'),
    dcc.Graph(id='pesticide-state-graph')
])

app.layout = county_graph

#tentativa de agrupar os condados e somar a quantidade de pesticidas
'''
@app.callback(
    Output(component_id= 'pesticide-state-graph', component_property='figure'),
    Input(component_id='pesticide-state-dropdown', component_property='value')
)
def update_state_graph(selected_compound):
    filtered_pesticide = pesticide_grouped[pesticide_grouped['COMPOUND'] == selected_compound]
    bar_fig = px.bar(filtered_pesticide,
                        x = 'STATE', y = 'HIGH_ESTIMATE',
                        title = 'QUANTIDADE ESTIMADA DE PESTICIDA',
                        barmode="group")
'''

@app.callback(
    Output(component_id= 'pesticide-county-graph', component_property='figure'),
    Input(component_id='pesticide-county-dropdown', component_property='value')
)
def update_county_graph(selected_compound):
    filtered_pesticide = pesticide[pesticide['COMPOUND'] == selected_compound]
    bar_fig = px.bar(filtered_pesticide,
                        x = 'COUNTY', y = 'HIGH_ESTIMATE',
                        title = 'QUANTIDADE ESTIMADA DE PESTICIDA',
                        barmode="group")

    return bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)