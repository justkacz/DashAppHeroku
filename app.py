import dash
from dash import dash_table
from dash.dash_table.Format import Format, Scheme, Trim
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df=pd.read_csv("https://raw.githubusercontent.com/justkacz/csvfiles/main/webvisitors3.csv",parse_dates=['date'])
df.date=pd.to_datetime(df.date)
df['month']=df.date.dt.month_name()


df=df[(df.value>=df.value.quantile(0.025))]
df=df[(df.value<=df.value.quantile(0.975))]


app.layout = html.Div(children=[
      html.Div(children=[
          html.P("Plotly | Dash", style={'margin': '0px'})
    ], className="header"),
      html.Div(children=[
          # html.Br(),
          dcc.Markdown(">Dashboard **presents**: bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla cdn.",style={'padding': '30px 20px 30px 20px', 'color':'rgb(92, 91, 91)'}),
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
            input_checked_class_name ='char-btn-ich',
            inline=True)
    ], className="sidebar1"),
      html.Div(children=[
      dcc.Graph(id='boxplot', style=dict(margin='1%', width='98%'))
    ], className="sidebar2"),
      html.Div([
      dbc.Tabs(id="tabs-example-graph", active_tab='tab-1-example-graph', className='custom-tabs-container', children=[
        dbc.Tab(label='Daily', tab_id='tab-1-example-graph'),
        dbc.Tab(label='Weekly', tab_id='tab-2-example-graph'),
        dbc.Tab(label='Monthly', tab_id='tab-3-example-graph')]),
      html.Div(id='tabs-content-example-graph'),
      # dcc.Markdown(id='markdown1',style={'padding': '30px 20px 10px 20px','color':'#7a8188',  "white-space": "pre-line"})   
      dbc.CardGroup([ 
        dbc.Card(
               dbc.CardBody([
                       html.P("Total number of visits: ", className="card-title"),
                      #  html.Hr(style={'border': "solid", "border-color": "rgba(240, 159, 10, 0.788)"}),
                       dcc.Markdown(id='markdown1', className="card-text"),
                       dcc.Markdown(id='markdown3', className="card-percent")
                   ])
              #  dbc.CardFooter([html.P(id='markdown3',className="card-title")])
          ),
        dbc.Card(
              dbc.CardBody([
                      html.P("Avg no. of visits per day: ", className="card-title"),
                      dcc.Markdown(id='markdown2', className="card-text"),
                      dcc.Markdown(id='markdown6', className="card-percent")
                      # html.Hr(style={'border': "solid", "border-color": "rgba(240, 159, 10, 0.788)"})
                  ])
          ),
        dbc.Card(
              dbc.CardBody([
                      html.P("The most popular weekday: ", className="card-title"),
                      dcc.Markdown(id='markdown4', className="card-text"),
                      dcc.Markdown(id='markdown5', className="card-percent")
                  ])
              # dbc.CardFooter("This is the footer"),
          )
        ])
     #close CardGroup
    ], className="content")
], className="container")


@app.callback(Output('tabs-content-example-graph', 'children'),
              Output('markdown1', 'children'),
              Output('markdown2', 'children'),
              Output('markdown3', 'children'),
              Output('markdown4', 'children'),
              Output('markdown5', 'children'),
              Output('markdown6', 'children'),
              Input('tabs-example-graph', 'active_tab'),
              Input('year-slider', 'value'),
              Input('dropdown', 'value'),
              Input('checklist', 'value'))
def render_content(tab, selected_year, device, selection):

    filtered_df=df[df.year.between(selected_year[0],selected_year[1], inclusive=True)]

    filtered_df_pie=filtered_df.copy()

    total_value=df.value.sum()
    # total_visits= "In selected period the number of visits was {}.".format(filtered_df.value.sum())
    pullval=np.array([0.05]*len(filtered_df_pie))

    if device is None:
      # if selection=='all':
        # filtered_df=filtered_df
      # else:
      if selection!='all':
        filtered_df=filtered_df[filtered_df.sex==selection]
        filtered_df_pie=filtered_df_pie[filtered_df_pie.sex==selection]
    else:
      if selection=='all':
          filtered_df=filtered_df[filtered_df.device==device]
      else:
          filtered_df=filtered_df[(filtered_df.sex==selection)&(filtered_df.device==device)]
          filtered_df_pie=filtered_df_pie[filtered_df_pie.sex==selection]
      idx=np.where(filtered_df_pie.device.values==device)
      pullval[idx[0][0]]=0.3

    filtered_df_month=filtered_df.groupby(filtered_df.date.dt.month_name()).sum()
    filtered_df_month.index = pd.CategoricalIndex(filtered_df_month.index, 
                               categories=['January', 'February', 'March','April','May', 'June','July','August','September','October','November','December'],
                               ordered=True)
    filtered_df_month=filtered_df_month.sort_index()
    filtered_df_month['change']=filtered_df_month.value.pct_change().fillna('-')
    filtered_df_month.reset_index(inplace=True)

    total_visits=filtered_df.value.sum()
    total_visits_perc=round((filtered_df.value.sum()/total_value)*100,2)
    avg_total_visits=round(filtered_df.value.sum()/len(filtered_df.date.unique()))
    avg_total_visits_perc=(avg_total_visits/total_visits)*100
    total_device=filtered_df['value'].groupby(filtered_df.device).sum().idxmax()
    total_sex=filtered_df['value'].groupby(filtered_df.sex).sum().idxmax()
    total_weekday=filtered_df['value'].groupby(filtered_df.day).sum().idxmax()
    total_weekday_perc=round((filtered_df.groupby(['day'])['value'].sum()/filtered_df.value.sum()).max()*100,2)

    p1= "**{:,d}**".format(total_visits)
    p2="**{:,d}**".format(avg_total_visits)
    p3="**{:.2f}%**".format(total_visits_perc)
    p4="**{}**".format(total_weekday)
    p5="**{:.2f}%**".format(total_weekday_perc)
    p6="**{:.2f}%**".format(avg_total_visits_perc)

    
    hovertemp = "Date: <b>%{x}</b><br>"
    hovertemp += "No. visits: <b>%{y}</b><br>"
    fig = px.line(filtered_df, x='date', y='value', color='device', symbol='device', color_discrete_sequence=['rgb(7, 83, 83)', 'grey'], height=320).update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hoverlabel=dict(
                bgcolor="rgba(247, 246, 242, 0.2)",
                bordercolor="rgba(247, 246, 242, 0.6)",
                font=dict(size=9, color='rgb(140, 139, 137)', family="Raleway")),
            xaxis=dict(title='Year', titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)', showgrid=False),
            yaxis=dict(title='Number of visits', titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)', showgrid=False),
            legend=dict(title=None, font=dict(size=8, color='rgb(193, 194, 194)')),
            margin=dict(l=0, r=30, t=0, b=0)).update_traces(
            hovertemplate=hovertemp, marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1))
    # fig3=px.histogram(filtered_df, x='value', nbins=80, color_discrete_sequence=['rgba(23, 151, 151, 0.2)', 'grey'], height=130).update_layout(
            # paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(titlefont_size=9, tickfont_size=9, color='rgb(193, 194, 194)', showgrid=False),yaxis=dict(titlefont_size=9, tickfont_size=9, showgrid=False, color='rgb(193, 194, 194)'), margin=dict(l=60, r=10, t=10, b=1)).update_traces(
            # marker=dict(line_width=1.5, line_color='rgb(23, 151, 151)'))
    fig4=px.histogram(filtered_df, x='year', y='value', color='day', text_auto=True, barmode='group', height=320, color_discrete_sequence=['rgba(7, 83, 83, 0.5)'], 
            category_orders={'day': ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday', 'Sunday']}).update_layout(
            margin=dict(l=30, r=0, t=20, b=0), yaxis_title='Number of visits',
            hoverlabel=dict(bgcolor="rgba(92, 91, 91, 0.6)", font_size=9,font_family="Raleway"), 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(title='Year', titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)', dtick=1), 
            yaxis=dict(titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)', gridcolor='rgba(193, 194, 194, 0.2)'), 
            legend=dict(title=None, font=dict(size=7, color='rgb(193, 194, 194)'))).update_traces(
            marker=dict(line_width=1.2, line_color='rgb(23, 151, 151)'))
    fig4.add_hline(np.mean(filtered_df.groupby(['year', 'day']).sum()).value, line_color="rgb(240, 111, 37)", line_width=1, opacity=1,line_dash="dot")
    fig4.add_annotation(text="mean", x=0, xref='paper',xanchor='right', y=np.mean(filtered_df.groupby(['year', 'day']).sum()).value,showarrow=False, font=dict(color="rgb(240, 111, 37)", size=9))
    
    collfill=np.array(['rgba(23, 151, 151,0.2)']*len(filtered_df_pie), dtype=object)
    colltext=np.array(['rgb(193, 194, 194)']*len(filtered_df_pie), dtype=object)
    # select device with max & min values:
    maxdev=filtered_df_pie.groupby('device')['value'].sum().idxmax()
    mindev=filtered_df_pie.groupby('device')['value'].sum().idxmin()
    idxmax=np.where(filtered_df_pie.device.values==maxdev)
    idxmin=np.where(filtered_df_pie.device.values==mindev)
    colltext[idxmax[0][0]]='rgba(76, 181, 158, 0.9)'
    # colltext[idxmax[0][0]]='rgb(112, 16, 40)'
    colltext[idxmin[0][0]]='rgba(232, 100, 95, 0.9)'
    # colltext[idxmin[0][0]]='rgba(232, 7, 44, 0.7)'

    min_monthly=filtered_df_month.value.min()

    fig5 = px.pie(data_frame=filtered_df_pie, values='value', names='device', color_discrete_sequence=collfill, height=350, hole=0.5)
    fig5.update_traces(textposition='outside', textinfo='percent+label', texttemplate='   %{label}   <br>   %{percent}   ', textfont_size=9, textfont_color=colltext,
                        marker=dict(line_width=1.2, line_color='rgb(23, 151, 151)'),
                        pull=pullval)
    # fig5.update_traces(textposition='outside',marker=dict(colors=['gold', 'mediumturquoise', 'darkorange', 'lightgreen'], line=dict(color='rgb(23, 151, 151)', width=2)))
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                        margin=dict(l=0, r=0, t=0, b=0))                      

    if tab == 'tab-1-example-graph':
        return dbc.Row(dcc.Graph(figure=fig, style=dict(margin='1%'))), p1, p2, p3, p4, p5, p6
    elif tab == 'tab-2-example-graph':
        return dbc.Row(dcc.Graph(figure=fig4, style=dict(margin='2%')), className='hist2'), p1, p2, p3, p4, p5, p6
    elif tab == 'tab-3-example-graph':
        return dbc.Row([
            dbc.Col(dcc.Graph(figure=fig5, style=dict(margin='2%'), className='pie')),
            dbc.Col(
                 dash_table.DataTable(
                     data=filtered_df_month.to_dict('records'),
                    #  columns=[{"name": i, "id": i} for i in filtered_df_month.columns],
                     columns=[dict(name= 'month', id= 'date'),
                              dict(name= 'value', id= 'value', type='numeric', format=Format().group(True)),
                              dict(name= 'change', id= 'change', type='numeric', format=Format(precision=2, scheme=Scheme.percentage))],
                     style_table={'hover':'red','marginTop':'10px', 'width':'100%'},
                     style_cell={'backgroundColor': 'rgba(0,0,0,0)', 'textAlign': 'center', 'border': '1px solid rgba(88,96,105, 0.4)'},
                     style_header={'backgroundColor':'rgba(27, 27, 27, 0.25)', 'color':'rgba(245, 114, 26, 0.4)','textShadow': '1px 1px 2px rgba(245, 114, 26, 0.4)', 'fontWeight':'bold', 'fontSize':'9px', 'border':'None'},
                     style_data={'margin':'0px','color': 'rgba(193, 194, 194, 0.9)', 'fontSize':'8px'},
                     style_as_list_view=True,
                     style_data_conditional=[{
                                  'if': {
                                        'filter_query': '{change} < 0',
                                        'column_id': 'change'
                                        },
                                    # 'color': 'rgb(232, 100, 95)',
                                    'color': 'rgba(232, 100, 95, 0.7)',
                                    'backgroundColor': 'rgba(89, 27, 25, 0.2)'
                                    # },
                                    # {
                                  # 'if': {
                                        # 'filter_query': '{value} == min_monthly',
                                        # 'column_id': 'value'
                                      #  },
                                  #  'color': 'rgb(232, 100, 95)',
                                  #  'color': 'rgba(232, 100, 95, 0.7)',
                                  #  'backgroundColor': 'rgba(89, 27, 25, 0.2)'
                                   }]
                      ), width=4)
        ]), p1, p2, p3, p4, p5, p6
       
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
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(title='Device', titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)'),
            yaxis=dict(title='Number of visits', titlefont_size=9, tickfont_size=9, titlefont_color='#586069',color='rgb(193, 194, 194)', gridcolor='rgba(193, 194, 194, 0.2)')).update_traces(
            marker=dict(size=2, color='rgb(23, 151, 151)'), line=dict(width=1, color='rgb(23, 151, 151)'))


    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)