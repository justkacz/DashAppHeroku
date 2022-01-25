import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df=pd.read_csv("https://raw.githubusercontent.com/justkacz/webvisitors/main/webvisitors3.csv",parse_dates=['date'])

df=df[(df.value>=df.value.quantile(0.025))]
df=df[(df.value<=df.value.quantile(0.975))]


app.layout = html.Div(children=[
      html.Div(children=[
          html.P("Plotly | Dash", style={'margin': '0px'})
    ], className="header"),
      html.Div(children=[
          # html.Br(),
          dcc.Markdown(">Dashbord **presents**: bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla cdn.",style={'padding': '30px 20px 30px 20px', 'color':'rgb(92, 91, 91)'}),
        #   html.Br(),
          html.P("Filter data by year:",style={'padding': '15px 20px'}),
          dcc.RangeSlider(
            id='year-slider',
            min=df.date.dt.year.min(),
            max=df.date.dt.year.max(),
            value=[df.date.dt.year.min(),df.date.dt.year.max()],
            marks={str(year): str(year) for year in df.date.dt.year.unique()},
            step=None,
            className="slider"
            ),
          html.P("Filter data by device:",style={'padding': '50px 20px 0px 20px'}),
          dcc.Dropdown(
            id='dropdown',
            options=[
               {'label': i, 'value' : i} for i in df.device.unique()
            ],
            multi=False,
            value='laptop',
            style=dict(),
            className="dropdownCSS"
            ),
          html.P("Filter data by gender:",style={'padding': '50px 20px 0px 20px'}),
          dbc.RadioItems(
            id='checklist',
            options=[
                {'label':'all', 'value':'all'},
                {'label':'female', 'value':'female'},
                {'label':'male', 'value':'male'}
                # {'label': i, 'value' : i} for i in df.sex.unique()
            ],
            value='all',
            className='char-btn',
            # inputClassName='char-btn-i',
            # labelClassName='char-btn-l',
            input_checked_class_name ='char-btn-ich',
            inline=True)
            # label_style={'padding': '5%', 'cursor':'pointer', 'text-align': 'center'},
            # inputStyle={'background-color': 'red'},
            # style={'text-align': 'center', 'padding-bottom': '2%'})
    ], className="sidebar1"),
      html.Div(children=[
      dcc.Graph(id='boxplot', style=dict(margin='1%', width='98%'))
    ], className="sidebar2"),
      html.Div([
      dcc.Tabs(id="tabs-example-graph", parent_className='custom-tabs', className='custom-tabs-container', value='tab-1-example-graph', children=[
        dcc.Tab(label='Line chart', value='tab-1-example-graph', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label='Bar chart', value='tab-2-example-graph', className='custom-tab', selected_className='custom-tab--selected')]),
      html.Div(id='tabs-content-example-graph'),
      # dcc.Markdown(id='markdown1',style={'padding': '30px 20px 10px 20px','color':'#7a8188',  "white-space": "pre-line"})
      dbc.Row([     
        dbc.Col(dbc.Card([
               dbc.CardBody([
                       html.P("Number of visits ", className="card-title"),
                      #  html.Hr(style={'border': "solid", "border-color": "rgba(240, 159, 10, 0.788)"}),
                       dcc.Markdown(id='markdown1', className="card-text"),
                       dcc.Markdown(id='markdown3', className="card-percent")
                   ]),
              #  dbc.CardFooter([html.P(id='markdown3',className="card-title")])
          ])),
        dbc.Col(dbc.Card([
              dbc.CardBody([
                      html.P("Avg no. of visits per day: ", className="card-title"),
                      dcc.Markdown(id='markdown2', className="card-text"),
                      # html.Hr(style={'border': "solid", "border-color": "rgba(240, 159, 10, 0.788)"})
                  ])
          ])),
        dbc.Col(dbc.Card([
              dbc.CardBody([
                      html.P("Avg number of visits per day: ", className="card-title"),
                      dcc.Markdown(id='markdown4', className="card-text")
                  ]),
              dbc.CardFooter("This is the footer"),
          ]))
        ])
    ], className="content"),
], className="container")


@app.callback(Output('tabs-content-example-graph', 'children'),
              Output('markdown1', 'children'),
              Output('markdown2', 'children'),
              Output('markdown3', 'children'),
              # Output('markdown4', 'children'),
              Input('tabs-example-graph', 'value'),
              Input('year-slider', 'value'),
              Input('dropdown', 'value'),
              Input('checklist', 'value'))
def render_content(tab, selected_year, device, selection):

    filtered_df=df[df.year.between(selected_year[0],selected_year[1], inclusive=True)]
    total_value=df.value.sum()
    # total_visits= "In selected period the number of visits was {}.".format(filtered_df.value.sum())

    if device is None:
      if selection=='all':
        filtered_df=filtered_df
      else:
        filtered_df=filtered_df[filtered_df.sex==selection]
    else:
      if selection=='all':
        filtered_df=filtered_df[filtered_df.device==device]
      else:
        filtered_df=filtered_df[(filtered_df.sex==selection)&(filtered_df.device==device)]
   
    total_visits=filtered_df.value.sum()
    total_visits_perc=round((filtered_df.value.sum()/total_value)*100,2)
    avg_total_visits=round(filtered_df.value.sum()/len(filtered_df.date.unique()))
    total_device=filtered_df['value'].groupby(filtered_df.device).sum().idxmax()
    total_sex=filtered_df['value'].groupby(filtered_df.sex).sum().idxmax()
    total_weekday=filtered_df['value'].groupby(filtered_df.day).sum().idxmax()

    p1= "**{:,d}**".format(total_visits)
    p2="**{:,d}**".format(avg_total_visits)
    p3="**{:.2f}%**".format(total_visits_perc)
    # p4=

    
    hovertemp = "Date: <b>%{x}</b><br>"
    hovertemp += "No. visits: <b>%{y}</b><br>"
    fig = px.line(filtered_df, x='date', y='value', color='device', symbol='device', color_discrete_sequence=['rgb(7, 83, 83)', 'grey'], height=350).update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hoverlabel=dict(
                bgcolor="rgba(247, 246, 242, 0.2)",
                bordercolor="rgba(247, 246, 242, 0.6)",
                font=dict(size=9, color='rgb(140, 139, 137)', family="Raleway")),
            yaxis_title=None,
            xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),
            yaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),
            legend=dict(title=None, font=dict(size=8, color='rgb(193, 194, 194)')),
            margin=dict(l=0, r=0, t=0, b=0)).update_traces(
            hovertemplate=hovertemp, marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1))
    # fig3=px.histogram(filtered_df, x='value', nbins=80, color_discrete_sequence=['rgba(23, 151, 151, 0.2)', 'grey'], height=130).update_layout(
            # paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),yaxis=dict(titlefont_size=9, tickfont_size=9, showgrid=False, color='rgb(193, 194, 194)'), margin=dict(l=60, r=10, t=10, b=1)).update_traces(
            # marker=dict(line_width=1.5, line_color='rgb(23, 151, 151)'))
    fig4=px.histogram(filtered_df, x='year', y='value', color='day', text_auto=True, barmode='group', height=350, color_discrete_sequence=['rgba(7, 83, 83, 0.5)'], 
            category_orders={'day': ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday', 'Sunday']}).update_layout(
            margin=dict(l=30, r=0, t=20, b=0), yaxis_title=None,
            hoverlabel=dict(bgcolor="rgba(92, 91, 91, 0.6)", font_size=9,font_family="Raleway"), 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, dtick=1, color='rgb(193, 194, 194)'), yaxis=dict( titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', gridcolor='rgba(193, 194, 194, 0.2)'), 
            legend=dict(title=None, font=dict(size=7, color='rgb(193, 194, 194)'))).update_traces(
            marker=dict(line_width=1.2, line_color='rgb(23, 151, 151)'))
    fig4.add_hline(np.mean(filtered_df.groupby(['year', 'day']).sum()).value, line_color="rgb(240, 111, 37)", line_width=1, opacity=1,line_dash="dot")
    fig4.add_annotation(text="mean", x=0, xref='paper',xanchor='right', y=np.mean(filtered_df.groupby(['year', 'day']).sum()).value,showarrow=False, font=dict(color="rgb(240, 111, 37)", size=9))

    if tab == 'tab-1-example-graph':
        return html.Div([
        dcc.Graph(figure=fig, style=dict(margin='2%', width='98%'))
        # dcc.Graph(figure=fig3, style=dict(margin='1%', width='98%'))
        ]), p1, p2, p3#, p4
    elif tab == 'tab-2-example-graph':
        return html.Div([
        dcc.Graph(figure=fig4, style=dict(margin='2%', width='98%'), className='hist2')
        ]), p1, p2, p3#, p4

@app.callback(     
     Output('boxplot', 'figure'),
     Input('year-slider', 'value'),
     Input('dropdown', 'value'),
     Input('checklist', 'value')
    )
            
def update_figure2(selected_year, device, selection):
    filtered_df2=df[df.year.between(selected_year[0],selected_year[1], inclusive=True)]

    if device is None:
      if selection=='all':
        filtered_df2=filtered_df2
      else:
        filtered_df2=filtered_df2[filtered_df2.sex==selection]
    else:
      if selection=='all':
        filtered_df2=filtered_df2[filtered_df2.device==device]
      else:
        filtered_df2=filtered_df2[(filtered_df2.sex==selection)&(filtered_df2.device==device)]

    
    fig2 = px.box(filtered_df2, x="device", y="value", color_discrete_sequence=['rgb(23, 151, 151)', 'grey']).update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)'),yaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', gridcolor='rgba(193, 194, 194, 0.2)')).update_traces(
            marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1, color='rgb(23, 151, 151)'))


    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)