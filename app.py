import os

from pandas.io.formats import style
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
server = app.server

df=pd.read_csv("https://raw.githubusercontent.com/justkacz/FreeCodeCampCert/main/fcc-forum-pageviews.csv", parse_dates=['date'])
s=['tablet', 'laptop', 'mobile', 'other']
df['device']=np.random.choice(s, size=1304)
df['year']=df.date.dt.year
df=df[(df.value>=df.value.quantile(0.025))]
df=df[(df.value<=df.value.quantile(0.975))]

app.layout = html.Div(children=[
      html.Div(children=[
        html.P("Plotly | Dash", style={'textAlign': 'center'})
    ], className="header"),
      html.Div(children=[
        html.P("Filter data by year:",style={'padding': '20px 20px'}),
        dcc.RangeSlider(
            id='year-slider',
            min=df.date.dt.year.min(),
            max=df.date.dt.year.max(),
            value=[df.date.dt.year.min(),df.date.dt.year.max()],
            marks={str(year): str(year) for year in df.date.dt.year.unique()},
            step=None,
            className="slider"
            ),
        html.P("Filter data by device:",style={'padding': '60px 20px 10px 20px'}),
        dcc.Dropdown(
            id='dropdown',
            options=[
               {'label': i, 'value' : i} for i in df.device.unique()
            ],
            multi=False,
            value='laptop',
            style=dict(),
            className="dropdownCSS"
            )
    ], className="sidebar1"),
      html.Div(children=[
        dcc.Graph(id='boxplot', style=dict(margin='1%', width='98%'))
    ], className="sidebar2"),
      html.Div(children=[
        # dcc.Graph(figure=fig, style=dict(padding='20px'))
        dcc.Graph(id='graph-with-slider', style=dict(margin='1%', width='98%')),
        dcc.Graph(id='hist', style=dict(margin='1%', width='98%'))
    ], className="content"),
], className="container")

@app.callback(
  Output('graph-with-slider', 'figure'),
  Output('boxplot', 'figure'),
  Output('hist', 'figure'),
  Input('year-slider', 'value'),
  Input('dropdown', 'value')
  )
def update_figure(selected_year, device):
    filtered_df=df[df.year.between(selected_year[0],selected_year[1], inclusive=True)]
    if device is not None:
        filtered_df = filtered_df[filtered_df.device==device]

    fig = px.line(filtered_df, x='date', y='value', color='device', symbol='device', color_discrete_sequence=['rgb(7, 83, 83)', 'grey'], height=350).update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hoverlabel=dict(
                bgcolor="rgba(0,0,0,0)",
                font_size=9,
                font_family="Raleway"),
            xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),
            yaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),
            legend=dict(font=dict(size=8, color='rgb(193, 194, 194)')),
            margin=dict(l=60, r=10, t=10, b=1)).update_traces(
            marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1))
    fig2 = px.box(filtered_df, x="device", y="value", color_discrete_sequence=['rgb(23, 151, 151)', 'grey']).update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)'),yaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', gridcolor='rgba(193, 194, 194, 0.2)')).update_traces(
            marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1, color='rgb(23, 151, 151)'))
    fig3=px.histogram(filtered_df, x='value', nbins=80, color_discrete_sequence=['rgba(23, 151, 151, 0.2)', 'grey'], height=130).update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),yaxis=dict(titlefont_size=9, tickfont_size=9, showgrid=False, color='rgb(193, 194, 194)'), margin=dict(l=60, r=10, t=10, b=1)).update_traces(
            marker=dict(line_width=1.5, line_color='rgb(23, 151, 151)'))

    return fig, fig2, fig3
#   return fig, dbc.Table.from_dataframe(filtered_df.head(10), striped=True, bordered=True, hover=True, color='dark')


if __name__ == '__main__':
    app.run_server(debug=True)








# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
# df=px.data.gapminder()
# 
# app = dash.Dash(__name__, title='Weekly Analytics', external_stylesheets=[dbc.themes.BOOTSTRAP])
# 
# server = app.server
# 
# def generate_table(dataframe, max_rows=10):
    # return html.Table(
        # Header
        # [html.Tr([html.Th(col) for col in dataframe.columns])] +
# 
        # Body
        # [html.Tr([
            # html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        # ]) for i in range(min(len(dataframe), max_rows))]
    # )
# 
# app.layout = html.Div([
    #  html.H1("Test Dash Plotly Dashboard"),
    #  html.Label(['continent:'], style={'font-weight': 'bold', "text-align": "center"}),
    #  dcc.Dropdown(
    #  id='dropdown',
    #  options=[
        #  {'label': i, 'value' : i} for i in df.continent.unique()
    #  ],
    #  multi=False,
    #  style=dict(width='50%')
    #  ),
    #  html.Br(),
    #  dcc.Slider(
    #  id='year-slider',
    #  min=df['year'].min(),
    #  max=df['year'].max(),
    #  value=df['year'].min(),
    #  marks={str(year): str(year) for year in df['year'].unique()},
    #  step=None
    #  ),
    #  dcc.Graph(id='graph-with-slider', style=dict(width='50%')),
    #  dcc.Graph(id='mapa'),
    #  html.Br(),
    #  html.Br(),
    #  html.Div(id='table-container')
    # ], 
    # style=dict(display='inline-block'))
# 
# 
# 
# @app.callback(
    # [Output('graph-with-slider', 'figure'),
    # Output('mapa', 'figure'),
    # Output('table-container', 'children')],
    # [Input('year-slider', 'value'),
    # Input('dropdown', 'value')]
    # )
# def update_figure(selected_year, continent):
    # if continent is None:
        # filtered_df=df[df.year==selected_year]
    # else:
        # filtered_df = df[(df.year==selected_year)&(df.continent==continent)]
# 
    # fig = px.sunburst(filtered_df, path=['continent', 'country'], values='pop',
                #   color='lifeExp')       
                #  
    # fig.update_layout(transition_duration=500, paper_bgcolor='#2c2c2c')
# 
    # fig2 = px.scatter_geo(filtered_df, locations="iso_alpha", color="continent",
                    #  hover_name="country", size="pop",
                    #  projection="hammer")
# 
    # fig2.update_layout(transition_duration=500, paper_bgcolor='#2c2c2c')
    # fig2.update_geos( showcoastlines=False,
                # fitbounds="locations",
                # subunitcolor='white')
# 
    # return fig, fig2, dbc.Table.from_dataframe(filtered_df.head(10), striped=True, bordered=True, hover=True, color='dark')
# 
# if __name__ == '__main__':
    # app.run_server(debug=True)