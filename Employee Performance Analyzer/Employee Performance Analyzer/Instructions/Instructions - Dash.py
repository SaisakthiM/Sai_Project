"""

Dash : it is a free module developed by plotly for web UI interfaces.

To create a web interface : 
app = dash.Dash(__name__,external_stylesheets={dbc.themes.BOOTSTRAP})

app = dash.Dash(__name__,external_stylesheets={dbc.themes.BOOTSTRAP})

# App layout and design

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(html.H1("Employee Performance Analyzer"),width=15, className="text-Center my-5")
    ])
)

dbc.Row([
dbc.Col([
dbc.Card([
dbc.CardBody([
html.H4 ("Patient Demographics", className="card-title"), dcc.Dropdown(
])
})
])
id="gender-filter"
),
dcc.Graph id="age






















"""