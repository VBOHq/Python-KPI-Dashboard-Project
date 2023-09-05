import dash
from dash import Dash, html, dcc, Input, Output  # pip install dash
import plotly.express as px
import dash_ag_grid as dag                       # pip install dash-ag-grid
import dash_bootstrap_components as dbc          # pip install dash-bootstrap-components
import pandas as pd                              # pip install pandas
from dash import dash_table
import base64
from io import BytesIO

historical_data = pd.read_csv(r"C:\Users\USER\Desktop\All Desktop\Project financial statement_new\historical_data.csv")
income_statement_items=['Year','Revenue', '% Growth', 'Cost of Goods Sold (COGS)',
       'COGS as % of Revenue', 'Gross Profit', 'Gross Profit Margin %',
       'Depreciation', 'Amortization', 'SG&A Expenses', 'SG&A as % of Revenue',
       'Operating Income / EBIT', 'Operating Income / EBIT Margin %', 'EBITDA',
       'EBITDA Margin %', 'EBITDA Growth', 'Interest Expense',
       'Interest Income', 'Net Interest Expense', 'Other Income / (Expense)',
       'Pretax Income', 'Taxes', 'Tax Rate', 'Net Income', 'Net Margin %',
       'Net Income Growth']

balance_sheet_items=['Year','Cash', 'Accounts Receivable', 'Inventory',
       'Other Current Assets', 'Total Current Assets', 'Gross PP&E',
       'Accumulated Depreciation', 'Net PP&E', 'Other Assets', 'Goodwill',
       'Total Assets', 'Accounts Payable', 'Accrued Liabilities',
       'Other Current Liabilities', 'Total Current Liabilities',
       'Revolving Credit Facility', 'Term Loan', 'Unsecured Debt',
       'Other Liabilities', 'Total Liabilities', 'Retained Earnings',
       'Common Stock', 'Total Shareholders Equity',
       'Total Liabilities and Equity', 'Depreciation and Amortization',
       'Change in Other Liabilities']
cash_flow_items=['Year','Cash Flow from Operations',
       'Capital Expenditures', 'Asset Dispositions',
       'Cash Flow from Investing', 'Change in Unsecured Debt',
       'Cash Flow from Financing', 'Net Cash Flow', 'Beginning Cash Position',
       'Change in Cash Position', 'Ending Cash Position',
       'Cash Flow Before Revolver', 'Beginning Revolver Balance',
       '(Paydown) / Drawdown', 'Ending Revolver Balance', 'Interest Rate',
       'Term Loan Beginning Balance', 'Term Loan Ending Balance',
       'Unsecured Debt Beginning Balance', 'Unsecured Debt Ending Balance',
       'Total Interest Expense', 'Interest Earned on Cash']

income_KPI =['Revenue', '% Growth', 'Gross Profit Margin %',
        'SG&A Expenses', 'Operating Income / EBIT', 'Operating Income / EBIT Margin %', 'EBITDA Margin %', 'EBITDA Growth', 'Interest Expense',
       'Net Interest Expense', 'Net Income', 'Net Margin %','Net Income Growth']

balance_KPI =['Cash', 'Accounts Receivable', 'Inventory',
       'Gross PP&E', 'Net PP&E', 'Total Assets', 'Accounts Payable', 'Total Current', 'Retained Earnings','Total Shareholders Equity','Total Liabilities and Equity']

cashflow_KPI=['Operating Cash Flow Margin', 'Free Cash Flow' ]
    
    
 
    
# Create a Dash app
   
data_science_colors = {
    'background': '#f4f4f4',  # Light gray
    'text': '#333333',  # Dark gray
    'skyblue': '#0c74da'  # Data science blue
}

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = dbc.Container([
    html.Div(style={
    'backgroundColor': data_science_colors['background'], 'color': data_science_colors['text'], 'border': '#f0f8ff',  # Blue border
        'border-radius': '15px',  # Rounded corners
        'padding': '40px'}, children=[
      # Adjust height as needed
    html.Img(src="C:/Users/USER\Desktop/KPI_project/img/frozenfood_logo.jpg", alt='Company Logo', height=10),
    html.H1("FINANCIAL KPI DASHBOARD", style={'text-align':'center', 'background-color':'light gray','color':'#0c74da', "font-weight": "bold", "font-size": 22}),
    
    html.Br(),
        
    # Dropdown to select financial statement category
    dcc.Dropdown(
        id='data-category-dropdown',
        options=[
            {'label': 'Income Statement', 'value': 'income_statement'},
            {'label': 'Balance Sheet', 'value': 'balance_sheet'},
            {'label': 'Cash Flow', 'value': 'cash_flow'}
        ],
        value='income_statement',  # Default value
        clearable=False,
        style={"color":"lblue",'width': '40%'}
    ),
    
    # Dropdown to select line item for line graph
    dcc.Dropdown(id='line-item-dropdown', style={"backgroud-color":"blue",'width': '50%'}),
    html.Br(),
    html.H5("Key Performance Indicators (KPIs) and Line Graph", style={'text-align':'center', 'background-color':'light gray','color':'#0c74da', "font-weight": "bold"}),
    dbc.Row([
        # First column with KPI table
        dbc.Col(
            dcc.Loading(id="kpi-loading", type="default", children=[
                dash_table.DataTable(
                    id='kpi-table',
                    style_table={'overflowX': 'scroll'},
                    style_data_conditional=[{'if': {'row_index': 0}, 'backgroundColor': 'skyblue','fontWeight': 'bold' }]
                )
            ]),
            width="40%" ,md=6  # Adjust the width as needed
        ),
        # Second column with line graph
        dbc.Col(
            dcc.Graph(id='line-graph'),
            width="60%" ,md=6 # Adjust the width as needed
        )
    ]),
    # Line break between the Line Graph and Data Table
    html.Br(),
    html.H5("Historical Data",style={'text-align':'center', 'background-color':'light gray','color':'#0c74da', "font-weight": "bold"}),
    # Data Table
    dash_table.DataTable(
        id='data-table',
        style_table={'overflowX': 'scroll'},
        style_data_conditional=[
            {'if': {'column_id': 'Year'},
             'fontWeight': 'bold'},
        ],
    ),  
    
])
])
# Callback to update KPI table based on the selected financial statement category
@app.callback(
    Output("kpi-table", "data"),
    Input('data-category-dropdown', 'value')
)
def update_kpi_table(selected_category):
    if selected_category == 'income_statement':
        kpi_set = income_KPI
    elif selected_category == 'balance_sheet':
        kpi_set = balance_KPI
    elif selected_category == 'cash_flow':
        kpi_set = cashflow_KPI
    else:
        kpi_set = []

    # Create a dictionary with KPIs and their current values
    kpi_data = {}
    for kpi in kpi_set:
        current_value = historical_data[kpi].iloc[-1] if kpi in historical_data.columns else None
        kpi_data[kpi] = current_value

    return [kpi_data]

@app.callback(
    Output('line-item-dropdown', 'options'),
    Output('line-item-dropdown', 'value'),
    [Input('data-category-dropdown', 'value')]
)
def update_line_item_dropdown(selected_category):
    if selected_category == 'income_statement':
        line_items = income_statement_items
    elif selected_category == 'balance_sheet':
        line_items = balance_sheet_items
    elif selected_category == 'cash_flow':
        line_items = cash_flow_items
        
    dropdown_options = [{'label': item, 'value': item} for item in line_items]
    default_value = dropdown_options[1]['value']  # Default to the second item
    
    return dropdown_options, default_value

@app.callback(
    Output('data-table', 'columns'),
    Output('data-table', 'data'),
    Output('data-table', 'style_data_conditional'),  # Add this line
    Output('line-graph', 'figure'),
    [Input('data-category-dropdown', 'value'),
     Input('line-item-dropdown', 'value')]
)
def update_data_table_and_line_graph(selected_category, selected_line_item):
    if selected_category == 'income_statement':
        columns = income_statement_items
    elif selected_category == 'balance_sheet':
        columns = balance_sheet_items
    elif selected_category == 'cash_flow':
        columns = cash_flow_items
    
    updated_columns = [{'name': col, 'id': col} for col in columns]
    updated_data = historical_data[columns].to_dict('records')
    style_header = {
        'backgroundColor': 'skyblue',
        'fontWeight': 'bold',
        'color': 'white'
    }
    # Line Graph
    if selected_line_item in historical_data.columns:
        line_graph_data = historical_data[['Year', selected_line_item]]
        
        fig = px.line(line_graph_data, x='Year', y=selected_line_item, title=f'Trend of {selected_line_item}', template='plotly_dark'  )
        fig.update_xaxes(showgrid=False) 
    else:
        fig = px.line(title='No data available')
    
    # Style selected line item in the data table
    style_data_conditional = [
        {
            'if': {'column_id': col},
            'fontWeight': 'bold',
            'backgroundColor': 'yellow'
        }
        for col in columns if col == selected_line_item
    ]
    
    return updated_columns, updated_data, style_data_conditional, fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
  