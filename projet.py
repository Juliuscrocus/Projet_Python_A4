import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import time

# Créer l'application Dash
app = dash.Dash(__name__)

# Définir le layout initial
app.layout = html.Div(children=[
    html.H1(children='Prix de Dogecoin dans le temps'),
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component', interval=10000, n_intervals=0)
])

# Définir la fonction de mise à jour
@app.callback(dash.dependencies.Output('graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph(n):
    # Lecture du fichier valeurs.txt
    df = pd.read_csv('valeurs.txt', sep=';', names=['prix', 'date'])

    # Convertir la colonne date en datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d_%H-%M-%S')

    # Créer le graphique
    trace = go.Scatter(x=df['date'], y=df['prix'], mode='lines')

    layout = go.Layout(title='Prix de Dogecoin dans le temps')

    fig = go.Figure(data=[trace], layout=layout)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=4000, host='0.0.0.0')
