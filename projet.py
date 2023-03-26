import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Read the values.txt file
df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')

# Create the Dash app
app = dash.Dash(__name__)

# Define the initial layout
app.layout = html.Div(children=[
    html.H1(children='Dogecoin Price Dashboard', className='title'),
    html.Div(children=[
        dcc.Graph(id='price-graph', style={'width': '100%', 'height': '600px'}),
        dcc.Interval(id='interval-component', interval=10000, n_intervals=0)
    ], className='graph-card', style={'margin': 'auto', 'width': '80%', 'padding': '30px'}),
    html.Div(children=[
        dcc.Graph(id='volatility-graph', style={'width': '48%', 'height': '400px'}),
        dcc.Graph(id='percentage-change-graph', style={'width': '48%', 'height': '400px'})
       ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'width': '80%', 'margin': 'auto'}),
    html.Div(children=[
        html.Div([
            html.H3('Current Price', className='title'),
            html.H4(id='current-price')    
        ], style={'width': '33%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            html.H3('High / Low (24h)', className='title'),
            html.H4(id='high-low-24h')
        ], style={'width': '33%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            html.H3('Percentage Change (24h)', className='title'),
            html.H4(id='percentage-change-24h')
        ], style={'width': '33%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'width': '80%', 'margin': 'auto'})
])

# Define callback functions to update the graphs

@app.callback(Output('price-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_price_graph(n):
    # Read the values.txt file
    df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])
    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')

    fig_price = go.Figure(data=[go.Scatter(x=df['date'], y=df['prix'], mode='lines')])
    fig_price.update_layout(template='plotly_dark', title='Dogecoin Price (USD)')
    return fig_price

@app.callback(Output('volatility-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_volatility_graph(n):
    # Read the values.txt file
    df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])
    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')
    
    # Calculate volatility
    df['returns'] = np.log(df['prix']/ df['prix'].shift(1))
    df['volatility'] = df['returns'].rolling(window=24).std() * np.sqrt(24)
    fig_volatility = go.Figure(data=[go.Scatter(x=df['date'], y=df['volatility'], mode='lines')])
    fig_volatility.update_layout(template='plotly_dark', title='Volatility (24h)')

    return fig_volatility

@app.callback(Output('percentage-change-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_percentage_change_graph(n):
    # Read the values.txt file
    df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])
    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')
    
    df['pct_change'] = df['prix'].pct_change() * 100
    pos_pct_change = df[df['pct_change'] > 0]['pct_change'].sum()
    neg_pct_change = df[df['pct_change'] < 0]['pct_change'].sum()

    fig_pct_change = go.Figure(go.Pie(labels=['Positive Change', 'Negative Change'], values=[pos_pct_change, abs(neg_pct_change)]))
    fig_pct_change.update_layout(template='plotly_dark', title='Percentage Change (24h)')

    return fig_pct_change

@app.callback(Output('current-price', 'children'), Input('interval-component', 'n_intervals'))
def update_current_price(n):
    # Read the values.txt file
    df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])
    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')
    
    current_price = df['prix'].iloc[-1]
    return f"${current_price:.5f}"

@app.callback(Output('high-low-24h', 'children'), Input('interval-component', 'n_intervals'))
def update_high_low_24h(n):
    high_24h = df['prix'].iloc[-24:].max()
    low_24h = df['prix'].iloc[-24:].min()
    return f"${high_24h:.5f} / ${low_24h:.5f}"

@app.callback(Output('percentage-change-24h', 'children'), Input('interval-component', 'n_intervals'))
def update_percentage_change_24h(n):
    pct_change_24h = ((df['prix'].iloc[-1] - df['prix'].iloc[-25]) / df['prix'].iloc[-25]) * 100
    return f"{pct_change_24h:.2f}%"

if __name__ == '__main__':
    app.run_server(debug=True, port=4001, host='0.0.0.0')



