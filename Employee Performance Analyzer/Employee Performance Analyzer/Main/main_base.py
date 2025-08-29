import dash
import dash_bootstrap_components as dbc
from dash import dcc,Input,Output,html
import plotly.express as px
import pandas as pd

# Loading Data

def load_data():

    data = pd.read_csv("Employee.csv")
    
    # Converting CSV Numeric to pd.numeric
    data["Employee_ID"] = pd.to_numeric(data["Employee_ID"])
    data["Age"] = pd.to_numeric(data["Age"])
    data["Years_At_Company"] = pd.to_numeric(data["Years_At_Company"])
    data["Performance_Score"] = pd.to_numeric(data["Performance_Score"])
    data["Monthly_Salary"] = pd.to_numeric(data["Monthly_Salary"])
    data["Work_Hours_Per_Week"] = pd.to_numeric(data["Work_Hours_Per_Week"])
    data["Projects_Handled"] = pd.to_numeric(data["Projects_Handled"])
    data["Overtime_Hours"] = pd.to_numeric(data["Overtime_Hours"])
    data["Sick_Days"] = pd.to_numeric(data["Sick_Days"])
    data["Remote_Work_Frequency"] = pd.to_numeric(data["Remote_Work_Frequency"])
    data["Team_Size"] = pd.to_numeric(data["Team_Size"])
    data["Training_Hours"] = pd.to_numeric(data["Training_Hours"])
    data["Promotions"] = pd.to_numeric(data["Promotions"])
    data["Employee_Satisfaction_Score"] = pd.to_numeric(data["Employee_Satisfaction_Score"])
    
    # Converting CSV Date to pd.datetime
    
    data["Hire_Date"] = pd.to_datetime(data["Hire_Date"])
    
    return data
data = load_data()

# Creating the dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Figures 

team_size_by_department = data.groupby('Department')['Team_Size'].sum().reset_index()
fig = px.bar(
    team_size_by_department,
    y='Team_Size',
    title="Total Team Size per Department",
    color='Department',
    color_discrete_sequence=px.colors.qualitative.Set2
)

project_handled = data.groupby('Department')['Projects_Handled'].sum().reset_index()
fig1 = px.bar(
    project_handled,
    y='Projects_Handled',
    title="Projects Handled by each Department",
    color='Department',
    color_discrete_sequence=px.colors.qualitative.Set2
)

average_salary = data.groupby('Department')['Monthly_Salary'].median().reset_index()
fig2 = px.bar(
    average_salary,
    y='Monthly_Salary',
    title="Projects Handled by each Department",
    color='Department',
    color_discrete_sequence=px.colors.qualitative.Set2
)

promotions = data.groupby('Department')['Promotions'].sum().reset_index()
fig3 = px.bar(
    promotions,
    y='Promotions',
    title="Promotions at each Department",
    color='Department',
    color_discrete_sequence=px.colors.qualitative.Set2
)

# App layout and design

def count(x):
    counter = 0
    for y in x:
        counter += 1
    return counter

data_day = int((data["Work_Hours_Per_Week"]/7).mean())
data_age = data["Age"].mean()
data_no = count(data["Department"].unique())
total_employees = count(data["Employee_ID"])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Employee Performance Analyzer"),
            width={"size": 10, "offset": 1},
            className="text-center my-5"
        )
    ]),
    
    # Employee Statistics
    dbc.Row([
        # Left side columns
        dbc.Col([
            html.H3(f"Average Employee Hours in Office (In 24 Hours) : {data_day}", className="my-3 text-start"),
            html.H3(f"Average Age of an Employee : {data_age}", className="my-3 text-start"),
        ], width=6),

        # Right side columns
        dbc.Col([
            html.H3(f"Total No of Departments : {data_no}", className="my-3 text-end"),
            html.H3(f"Total No of Employees : {total_employees}", className="my-3 text-end"),
        ], width=6),
    ], className="mb-5"),
    
    # Employee Demographics
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Employee Demographics : Size of each Department",className="card-title"),
                    dcc.Dropdown(
                        id="size-filter"
                    ),
                    dcc.Graph(id='dep-distribution', figure=fig)
                ])
            ])
        ],width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Employee Demographics : Projects Handled by each Department",className="card-title"),
                    dcc.Dropdown(
                        id="performance-filter"
                    ),
                    dcc.Graph(id="performance-distribution",figure=fig1)
                ])
            ])
        ],width=6),
        
    ]),
    # No of employee at different Age
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("No of Employee at different Age",className="card-title"),
                    dcc.Slider(
                        id="age-slider",
                        min=data['Age'].min(),
                        max=data['Age'].max(),
                        value=data['Age'].median(),
                        marks={int(value):f"{int(value)}" for value in data["Age"].quantile([0,0.25,0.5,0.75,1]).values},
                        step=100
                    
                    
                    ),
                    dcc.Graph(id="members-each-dep")
                ])
            ])
        ],width=12)
    ]),
    # Promotion in each department
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("No of Promotion in each department",className="card-title"),
                    dcc.Dropdown(
                        id="promo-filter"
                    ),
                    dcc.Graph(id="department",figure=fig3)
                ])
            ])
        ],width=12)
    ]),
    # Average Department Employee Salary
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Average Salary at each department",className="card-title"),
                    dcc.Dropdown(
                        id="ave-filter"
                    ),
                    dcc.Graph(
                        id="salary",figure=fig2
                    )
                ])
            ])
        ],width=12)
    ])
], fluid=True)


# Create Our Callbacks

@app.callback(
    Output("members-each-dep", "figure"),
    Input("age-slider", "value")
)
def update_graph(selected_age):
    # Filter data for employees with Age <= selected value
    filtered_data = data[data["Age"] <= selected_age]

    # Group by Age and count the number of employees
    team_size_by_age = filtered_data.groupby("Age").size().reset_index(name="Team Size")

    # Create line chart
    fig = px.line(team_size_by_age, x="Age", y="Team Size",
                  markers=True,
                  labels={"Age": "Age", "Team Size": "Number of Employees"},
                  title=f"Team Size Distribution for Age ≤ {selected_age}")
    
    fig.update_traces(line=dict(color="red"))
    fig.update_layout(hovermode="x unified")

    return fig


















































if __name__ == '__main__':
    app.run(debug=True)