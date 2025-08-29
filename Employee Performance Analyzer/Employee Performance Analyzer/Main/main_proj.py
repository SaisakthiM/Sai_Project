import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load Data
def load_data():
    data = pd.read_csv("Employee.csv")
    numeric_cols = [
        "Employee_ID", "Age", "Years_At_Company", "Performance_Score", "Monthly_Salary",
        "Work_Hours_Per_Week", "Projects_Handled", "Overtime_Hours", "Sick_Days",
        "Remote_Work_Frequency", "Team_Size", "Training_Hours", "Promotions",
        "Employee_Satisfaction_Score"
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col])
    data["Hire_Date"] = pd.to_datetime(data["Hire_Date"])
    return data

# Initialize Data and App
data = load_data()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # CYBORG theme for modern dark look

# Helper Functions
def count_unique(x):
    return len(set(x))

# Precomputed Stats
data_day = int((data["Work_Hours_Per_Week"] / 7).mean())
data_age = round(data["Age"].mean(), 1)
data_no = count_unique(data["Department"])
total_employees = count_unique(data["Employee_ID"])

# Layout
app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("\ud83d\udcbc HR Dashboard", className="mx-auto text-info fw-bold fs-2")
        ]),
        color="dark", dark=True, className="mb-4 shadow"
    ),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H6("Avg. Daily Office Hours", className="text-muted text-center"),
                            dcc.Graph(
                                figure=px.pie(
                                    names=["Office Hours", "Remaining Time"],
                                    values=[data_day, 24 - data_day],
                                    hole=0.6,
                                    template="plotly_dark",
                                    color_discrete_sequence=px.colors.sequential.RdBu
                                ).update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                            )
                        ])
                    ])
                ]), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H6("Avg. Employee Age", className="text-muted text-center"),
                            dcc.Graph(
                                figure=go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=data_age,
                                    title={'text': "Age"},
                                    gauge={'axis': {'range': [20, 60]}},
                                    domain={'x': [0, 1], 'y': [0, 1]}
                                )).update_layout(
                                    template="plotly_dark",
                                    margin=dict(t=0, b=0, l=0, r=0)
                                )
                            )
                        ])
                    ])
                ]), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H6("Departments", className="text-muted text-center"),
                            dcc.Graph(
                                figure=px.bar(
                                    x=["Departments"], y=[data_no],
                                    template="plotly_dark",
                                    color_discrete_sequence=["#00CC96"]
                                ).update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
                            )
                        ])
                    ])
                ]), width=3),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H6("Total Employees", className="text-muted text-center"),
                            dcc.Graph(
                                figure=px.funnel(
                                    x=["Employees"], y=[total_employees],
                                    template="plotly_dark"
                                ).update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
                            )
                        ])
                    ])
                ]), width=3)
            ])
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Department-wise Team Size", className="card-title text-center mb-4 fs-4 fw-semibold"),
                    dcc.Graph(figure=px.bar(
                        data.groupby('Department')['Team_Size'].sum().reset_index(),
                        y='Team_Size', color='Department',
                        title="Total Team Size per Department",
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        template="plotly_dark"
                    ))
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Projects Handled by Department", className="card-title text-center mb-4 fs-4 fw-semibold"),
                    dcc.Graph(figure=px.area(
                        data.groupby('Department')['Projects_Handled'].sum().reset_index(),
                        x='Department', y='Projects_Handled',
                        title="Projects Handled by each Department",
                        template="plotly_dark",
                        color_discrete_sequence=px.colors.qualitative.Set2
                    ))
                ])
            ])
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Employees by Age (Adjust Slider)", className="card-title text-center mb-4 fs-4 fw-semibold"),
                    dcc.Slider(
                        id="age-slider",
                        min=data['Age'].min(),
                        max=data['Age'].max(),
                        value=data['Age'].median(),
                        marks={int(val): f"{int(val)}" for val in data["Age"].quantile([0, 0.25, 0.5, 0.75, 1])},
                        step=1
                    ),
                    dcc.Graph(id="members-each-dep")
                ])
            ])
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Promotions by Department", className="card-title text-center mb-4 fs-4 fw-semibold"),
                    dcc.Graph(figure=px.scatter(
                        data.groupby('Department')['Promotions'].sum().reset_index(),
                        x='Department', y='Promotions',
                        title="Promotions per Department",
                        template="plotly_dark",
                        color='Promotions', size='Promotions'
                    ))
                ])
            ])
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Median Salary by Department", className="card-title text-center mb-4 fs-4 fw-semibold"),
                    dcc.Graph(figure=px.treemap(
                        data.groupby('Department')['Monthly_Salary'].median().reset_index(),
                        path=['Department'], values='Monthly_Salary',
                        title="Average Salary by Department",
                        template="plotly_dark",
                        color='Monthly_Salary', color_continuous_scale='Viridis'
                    ))
                ])
            ])
        ])
    ])

], fluid=True)

# Callback
@app.callback(
    Output("members-each-dep", "figure"),
    Input("age-slider", "value")
)
def update_graph(selected_age):
    filtered = data[data["Age"] <= selected_age]
    team_size_by_age = filtered.groupby("Age").size().reset_index(name="Team Size")
    fig = px.line(team_size_by_age, x="Age", y="Team Size", markers=True,
                  title=f"Team Size Distribution for Age ≤ {selected_age}",
                  labels={"Age": "Age", "Team Size": "Number of Employees"},
                  template="plotly_dark")
    fig.update_traces(line=dict(color="red"))
    fig.update_layout(hovermode="x unified")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
