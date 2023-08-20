from dash import Dash, html, dcc, Input, Output  # pip install dash
import plotly.express as px
import dash_ag_grid as dag                       # pip install dash-ag-grid
import dash_bootstrap_components as dbc          # pip install dash-bootstrap-components
import pandas as pd                              # pip install pandas

import matplotlib                                # pip install matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

df = pd.read_csv(r"C:\Users\USER\Desktop\All Desktop\Project financial statement_new\historical_data.csv", index_col="Year")
income_statement_items=['Revenue', '% Growth', 'Cost of Goods Sold (COGS)',
       'COGS as % of Revenue', 'Gross Profit', 'Gross Profit Margin %',
       'Depreciation', 'Amortization', 'SG&A Expenses', 'SG&A as % of Revenue',
       'Operating Income / EBIT', 'Operating Income / EBIT Margin %', 'EBITDA',
       'EBITDA Margin %', 'EBITDA Growth', 'Interest Expense',
       'Interest Income', 'Net Interest Expense', 'Other Income / (Expense)',
       'Pretax Income', 'Taxes', 'Tax Rate', 'Net Income', 'Net Margin %',
       'Net Income Growth']

balance_sheet_items=['Cash', 'Accounts Receivable', 'Inventory',
       'Other Current Assets', 'Total Current Assets', 'Gross PP&E',
       'Accumulated Depreciation', 'Net PP&E', 'Other Assets', 'Goodwill',
       'Total Assets', 'Accounts Payable', 'Accrued Liabilities',
       'Other Current Liabilities', 'Total Current Liabilities',
       'Revolving Credit Facility', 'Term Loan', 'Unsecured Debt',
       'Other Liabilities', 'Total Liabilities', 'Retained Earnings',
       'Common Stock', 'Total Shareholders Equity',
       'Total Liabilities and Equity', 'Depreciation and Amortization',
       'Change in Other Liabilities']
cash_flow_items=['Cash Flow from Operations',
       'Capital Expenditures', 'Asset Dispositions',
       'Cash Flow from Investing', 'Change in Unsecured Debt',
       'Cash Flow from Financing', 'Net Cash Flow', 'Beginning Cash Position',
       'Change in Cash Position', 'Ending Cash Position',
       'Cash Flow Before Revolver', 'Beginning Revolver Balance',
       '(Paydown) / Drawdown', 'Ending Revolver Balance', 'Interest Rate',
       'Term Loan Beginning Balance', 'Term Loan Ending Balance',
       'Unsecured Debt Beginning Balance', 'Unsecured Debt Ending Balance',
       'Total Interest Expense', 'Interest Earned on Cash']
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Interactive Finance KPI Dashboard", className='mb-2', style={'text-align':'center', 'background-color':'light gray','color':'gold', "font-weight": "bold"}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='incomeStament',
                value='Revenue',
                clearable=False,
                options=income_statement_items)
        ], width=4),
       
        dbc.Col([
            dcc.Dropdown(
                id='BalanceSheet',
                value='Cash',
                clearable=False,
                options=balance_sheet_items)
        ], width=4),
        
        dbc.Col([
            dcc.Dropdown(
                id='CashFlow',
                value='Cash',
                clearable=False,
                options=balance_sheet_items)
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-incomeStatement')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-plotly', figure={})
        ], width='30%', md=6),
        dbc.Col([
            dag.AgGrid(
                id='grid',
                rowData=df.to_dict("records"),
                columnDefs=[{"field": i} for i in df.columns],
                columnSize="sizeToFit",
            )
        ], width='70%', md=6),
        html.Br(),
    ], className='mt-4'),
    dbc.Row([html.I("Copy Right Frozen Food",  style={'text-align': 'center', 'font-size':22, 'background-color':'sky blue'})])
], style={'text-align': 'center', 'font-size':12, 'background-color':'black', 'color':'white',"width": "80%", "margin": "0 auto", "padding": "20px",
           "@media screen and (max-width: 600px)": {"width": "100%"}
          })

# Create interactivity between dropdown component and graph
@app.callback(
    Output(component_id='bar-graph-incomeStatement', component_property='src'),
    Output('bar-graph-plotly', 'figure'),
    Output('grid', 'defaultColDef'),
    Input('incomeStatement', 'value'),
)
def plot_data(income_statement_item):

    # Build the matplotlib figure
    fig = plt.figure(figsize=(12, 5))
    plt.bar(df.index, df[income_statement_items])
    plt.ylabel(income_statement_items)
    plt.xticks(rotation=30)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    # Build the Plotly figure
    fig_bar_plotly = px.bar(df, x=df.index, y=income_statement_items).update_xaxes(tickangle=330)

    my_cellStyle = {
        "styleConditions": [
            {
                "condition": f"params.colDef.field == '{income_statement_items}'",
                "style": {"backgroundColor": "#d3d3d3"},
            },
            {   "condition": f"params.colDef.field != '{income_statement_items}'",
                "style": {"color": "black"}
            },
        ]
    }

    return fig_bar_matplotlib, fig_bar_plotly, {'cellStyle': my_cellStyle}


if __name__ == '__main__':
    app.run_server(debug=False, port=8002)





