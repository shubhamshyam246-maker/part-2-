# Final Assignment: Part 2 - Create Dashboard with Plotly and Dash

This script creates an interactive Dash application analyzing historical automobile sales data during recession and non-recession periods.

## Steps to Run this App:
1. Save this file as `automobile_sales_dashboard.py`
2. Install dependencies: `pip install dash pandas plotly`
3. Run the script: `python automobile_sales_dashboard.py`
4. Open your web browser and navigate to `http://127.0.0.1:8050/`

"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Create the layout of the app
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f9f9f9'}, children=[
    
    # TASK 2.1: Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': '28px', 'marginBottom': '20px'}
    ),
    
    # TASK 2.2: Add drop-down menus
    html.Div([
        html.Label("Select Report Type:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            style={'width': '300px', 'padding': '3px', 'fontSize': '16px'}
        )
    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
    
    html.Div([
        html.Label("Select Year:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': int(i), 'value': int(i)} for i in sorted(df['Year'].unique())],
            placeholder='Select a year',
            disabled=True,
            style={'width': '300px', 'padding': '3px', 'fontSize': '16px'}
        )
    ], style={'marginBottom': '25px', 'display': 'flex', 'alignItems': 'center'}),
    
    # TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'})
])

# Callback to enable/disable the Year Dropdown based on Report Type
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_report):
    if selected_report == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to generate plots based on selections
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_report, input_year):
    if not selected_report:
        return html.Div("Please select a report type to display graphs.", style={'color': '#888', 'fontSize': '16px', 'marginTop': '20px'})
        
    if selected_report == 'Recession Period Statistics':
        # Filter data for recession period
        recession_df = df[df['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate year over year during recession period
        yearly_rec = recession_df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                           title="Average Automobile Sales Fluctuation Over Recession Period",
                           labels={'Automobile_Sales': 'Average Sales'})
        )
        
        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type During Recession",
                          labels={'Automobile_Sales': 'Average Sales', 'Vehicle_Type': 'Vehicle Type'})
        )
        
        # Plot 3: Total expenditure share by vehicle type during recessions
        exp_rec = recession_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertising Expenditure Share by Vehicle Type During Recession")
        )
        
        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_df.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
                          title="Effect of Unemployment Rate on Vehicle Type and Sales Volume",
                          labels={'Automobile_Sales': 'Average Sales', 'Unemployment_Rate': 'Unemployment Rate'},
                          barmode='group')
        )
        
        # Structure charts in a 2x2 grid style using flexbox widths
        return [
            html.Div(R_chart1, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(R_chart2, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(R_chart3, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(R_chart4, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ]
        
    elif selected_report == 'Yearly Statistics':
        if not input_year:
            return html.Div("Please select a specific year to generate the yearly report charts.", style={'color': '#888', 'fontSize': '16px', 'marginTop': '20px'})
            
        # Filter data for the selected year
        yearly_df = df[df['Year'] == input_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        all_yearly = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(all_yearly, x='Year', y='Automobile_Sales',
                           title="Overall Yearly Automobile Sales Trend",
                           labels={'Automobile_Sales': 'Average Sales'})
        )
        
        # Plot 2: Total Monthly Sales for the selected year
        monthly_sales = yearly_df.groupby('Month')['Automobile_Sales'].sum().reset_index()
        # Sort months correctly if needed, mapping months can help, but keeping order as present in data grouped
        Y_chart2 = dcc.Graph(
            figure=px.line(monthly_sales, x='Month', y='Automobile_Sales',
                           title=f"Total Monthly Automobile Sales in the Year {input_year}",
                           labels={'Automobile_Sales': 'Total Sales'})
        )
        
        # Plot 3: Average Vehicles Sold per Vehicle Type in the selected year
        avr_vdata = yearly_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f"Average Vehicles Sold by Vehicle Type in the Year {input_year}",
                          labels={'Automobile_Sales': 'Average Sales', 'Vehicle_Type': 'Vehicle Type'})
        )
        
        # Plot 4: Total Advertisement Expenditure for each vehicle type using pie chart
        exp_year = yearly_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_year, values='Advertising_Expenditure', names='Vehicle_Type',
                          title=f"Total Advertisement Expenditure Share by Vehicle Type in {input_year}")
        )
        
        return [
            html.Div(Y_chart1, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(Y_chart2, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(Y_chart3, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            html.Div(Y_chart4, style={'width': '48%', 'minWidth': '400px', 'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ]

if __name__ == '__main__':
    app.run_server(debug=True)
"""
