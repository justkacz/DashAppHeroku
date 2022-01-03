import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash(__name__)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.Label(['Countries:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(
    options=[
        {'label': i, 'value' : i} for i in df.country.unique()
    ],
    multi=True,
    value="MLT",
    style=dict(width='50%')
    ),
    html.Label(['Continent:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(
    id='dropdown',
    options=[
      {'label': i, 'value' : i} for i in df.continent.unique()
    ],
    multi=True,
    value="MLT",
    style=dict(width='50%')
    ),
    # dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    html.Div(id='table-container')
])


@app.callback(
    Output('table-container', 'children'),
    # Output('graph-with-slider', 'figure'),
    # Input('year-slider', 'value')
    Input('dropdown', 'value')
    )
# def update_figure(selected_year):
    # filtered_df = df[df.year == selected_year]
# 
    # fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                    #  size="pop", color="continent", hover_name="country",
                    #  log_x=True, size_max=55)
# 
    # fig.update_layout(transition_duration=500)
    # return fig

def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    dff = df[df.country.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)



if __name__ == '__main__':
    app.run_server(debug=True)