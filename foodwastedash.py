import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# 加载数据集
file_path = "Food Waste data and research - by country (1).csv"
data = pd.read_csv(file_path)

# 按 'Household estimate (tonnes/year)' 从高到低排序
sorted_data = data[['Country', 'Household estimate (tonnes/year)']].sort_values(
    by='Household estimate (tonnes/year)', ascending=False)

# 分页设置
page_size = 10
num_pages = (len(sorted_data) + page_size - 1) // page_size

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Food Waste by Country (Household estimate in tonnes/year)'),
    dcc.Graph(id='food-waste-plot'),
    dcc.Dropdown(
        id='page-selector',
        options=[{'label': f'{i*page_size+1}-{min((i+1)*page_size, len(sorted_data))}', 'value': i} 
                 for i in range(num_pages)],
        value=0
    )
])

@app.callback(
    Output('food-waste-plot', 'figure'),
    Input('page-selector', 'value')
)
def update_graph(page):
    start = page * page_size
    end = start + page_size
    
    fig = go.Figure(go.Bar(
        x=sorted_data['Country'][start:end],
        y=sorted_data['Household estimate (tonnes/year)'][start:end],
        text=sorted_data['Household estimate (tonnes/year)'][start:end],
        textposition='outside',
        marker_color='#d6c4de'
    ))
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Household Estimate (tonnes/year)',
        template='plotly_white',
        height=600,
        margin=dict(l=50, r=50, t=50, b=100),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
