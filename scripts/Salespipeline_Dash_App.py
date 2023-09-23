import dash
from dash import Dash, dash_table, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as InnerHTML
import dash_daq as daq
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText


def SuperPixel(
    Monthly_Traffic,
    Cost_Per_Aquisition,
    Sales_Conversion_Rate,
    Deal_Value,
    Re_opt_in_percent,
    Re_activation_Sales_Rate,
    Cost_Per_Match_Re_activation,
    Verification_percent,
    ID_Resolution_Match_percent,
):
    Sales = Monthly_Traffic * Sales_Conversion_Rate
    Revenue = Sales * Deal_Value
    Estimated_Spend = Sales * Cost_Per_Aquisition
    Anonymous_Traffic = Monthly_Traffic - (Monthly_Traffic * Sales_Conversion_Rate)
    Consumer_Matches = Anonymous_Traffic * ID_Resolution_Match_percent
    Verified_Matched_Profiles = Consumer_Matches * Verification_percent
    Recovered_Leads = Verified_Matched_Profiles * Re_opt_in_percent
    Recovered_Sales = Recovered_Leads * Re_activation_Sales_Rate
    Recovered_Revenue = Recovered_Sales * Deal_Value
    Total = Cost_Per_Match_Re_activation * Recovered_Leads
    CPA_After = Total / Recovered_Sales

    calculated_values = {
        "Sales": Sales,
        "Revenue": Revenue,
        "Estimated Spend": Estimated_Spend,
        "Anonymous Traffic": int(Anonymous_Traffic),
        "Consumer Matches": int(Consumer_Matches),
        "Verified Matched_Profiles": int(Verified_Matched_Profiles),
        "Recovered Leads": int(Recovered_Leads),
        "Recovered Sales": Recovered_Sales,
        "Recovered Revenue": Recovered_Revenue,
        "Total": Total,
        "CPA(After)": CPA_After,
    }
    return calculated_values


# WastedSpend function
def WastedSpend(
    Sales,
    Data_Cleaning,
    Estimated_Spend,
    Pixel_Match_Rate,
    Platform_Match_Rate,
    Monthly_Traffic,
    Sales_Conversion_Rate,
    Price,
):
    profiles_FB_Google_Pixel_Captured = Monthly_Traffic * 0.15
    Revenue = Price * Sales
    Profit = Revenue - Sales
    Wasted_Spend = Estimated_Spend * 0.75
    Lost_Traffic_Total = Monthly_Traffic - (Monthly_Traffic * Sales_Conversion_Rate)
    Matched_Visitors = Pixel_Match_Rate * Lost_Traffic_Total
    Contactable_Leads = Data_Cleaning * Matched_Visitors
    Targetable_Pixeled_Audience = Platform_Match_Rate * Matched_Visitors

    wasted_spend_values = {
        "profiles_FB_Google_Pixel_Captured": profiles_FB_Google_Pixel_Captured,
        "Revenue": Revenue,
        "Profit": Profit,
        "Wasted_Spend": Wasted_Spend,
        "Lost_Traffic_Total": Lost_Traffic_Total,
        "Matched_Visitors": Matched_Visitors,
        "Contactable_Leads": Contactable_Leads,
        "Targetable_Pixeled_Audience": Targetable_Pixeled_Audience,
    }
    return wasted_spend_values


def AudienceBuilder(
    Ad_Spend,
    Average_Order_Value,
    Cost_per_1000_Impressions,
    Click_Through_Rate,
    Site_Conversion_Rate,
):
    Impressions_Needed = (Ad_Spend / Cost_per_1000_Impressions) * 1000
    Clicks = Impressions_Needed * Click_Through_Rate
    Total_Sales = Site_Conversion_Rate * Clicks
    CPA = Ad_Spend / Total_Sales
    Revenue = (Ad_Spend / CPA) * Average_Order_Value
    Total_Profit_After_Adspend = Revenue - Ad_Spend
    Cost_per_1_Impression = Cost_per_1000_Impressions / 1000

    audience_values = {
        "Impressions_Needed": Impressions_Needed,
        "Clicks": Clicks,
        "Total_Sales": Total_Sales,
        "CPA": CPA,
        "Revenue": Revenue,
        "Total_Profit_After_Adspend": Total_Profit_After_Adspend,
        "Cost_per_1_Impression": Cost_per_1_Impression,
    }

    return audience_values


def AffiliateLab(
    Your_Plan, Avg_Plan_Ref, Sales_Conversion_Rate, Response_Rate, Ref_Payout_Percent
):
    Payout = Ref_Payout_Percent * Avg_Plan_Ref
    Referrals_Needed_to_Be = Your_Plan * Payout
    Conversations_Needed = Referrals_Needed_to_Be * Sales_Conversion_Rate
    Touch_Points_Needed = Conversations_Needed * Response_Rate

    Affiliate_values = {
        "Payout": Payout,
        "Referrals_Needed_to_Be": Referrals_Needed_to_Be,
        "Conversations_Needed": Conversations_Needed,
        "Touch_Points_Needed": Touch_Points_Needed,
    }
    return Affiliate_values


def format_number(number):
    if not isinstance(number, (int, float)):
        raise ValueError("Invalid input type. Expected int or float.")

    if abs(number) < 1000:
        return f"${number:.1f}"
    if abs(number) < 1e6:
        return f"${number / 1e3:.1f}k"
    if abs(number) < 1e9:
        return f"${number / 1e6:.1f}M"
    if abs(number) < 1e12:
        return f"${number / 1e9:.1f}B"
    if abs(number) < 1e15:
        return f"${number / 1e12:.1f}Trillion"

    return str(number)


# function to send mail
def send_email(sender_email, sender_name, feedback):
    to_address = "tertimothy@gmail.com"
    password = "ikilyacpasuvfcgg"  # WARNING: Do not hardcode your password
    subject = f"Feedback from {sender_name}"

    msg = MIMEText(feedback)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_address

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_address, msg.as_string())
        server.quit()
        return "Feedback sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"


# function to generate dat table
def generate_table(df):
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "10px", "backgroundColor": "gray",},
        style_header={"fontWeight": "bold", "backgroundColor": "black"},
    )


# sidebar
def sidebar_main():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Label("Select Tab"),
                                    dcc.Dropdown(
                                        id="dropdown-menu",
                                        options=[
                                            {
                                                "label": "SuperPixel",
                                                "value": "SuperPixel",
                                            },
                                            {
                                                "label": "Wasted Spend Metrics",
                                                "value": "Wasted Spend Metrics",
                                            },
                                            {
                                                "label": "Audience Builder",
                                                "value": "Audience Builder",
                                            },
                                            {
                                                "label": "AffiliateLab",
                                                "value": "AffiliateLab",
                                            },
                                        ],
                                        value="SuperPixel",
                                        clearable=False,
                                    ),
                                    html.Div(id="dropdown-output"),
                                ],
                            ),
                            html.Hr(),
                        ]
                    ),
                ]
            )
        ]
    )


def tab():
    return html.Div(
        [
            dcc.Tabs(
                id="tabs-example",
                value="tab-1",
                children=[
                    dcc.Tab(label="SuperPixel", value="tab-1"),
                    dcc.Tab(label="Wasted Spend", value="tab-2"),
                    dcc.Tab(label="Audience Builder", value="tab-3"),
                    dcc.Tab(label="AffiliateLab", value="tab-4"),
                ],
            ),
            html.Div(id="tabs-content-example"),
        ]
    )


def body_main():
    return html.Div(
        [
            dbc.Card(
                dbc.CardBody([html.Div([tab(), html.Hr()])]),
                
            ),
            html.Hr(),
            html.Div(
                [
                    dbc.Button(
                        "Provide Feedback",
                        id="toggle-feedback",
                        className="mb-3",
                        color="primary",
                    ),
                    dbc.Collapse(
                        html.Div(
                            [
                                dbc.Input(
                                    id="user-name", placeholder="Your Name", type="text"
                                ),
                                dbc.Input(
                                    id="user-email",
                                    placeholder="Your Email",
                                    type="email",
                                ),
                                dbc.Textarea(
                                    id="feedback-text",
                                    placeholder="Enter your feedback...",
                                ),
                                dbc.Button(
                                    "Submit",
                                    id="submit-button",
                                    n_clicks=0,
                                    color="primary",
                                ),
                                html.Div(id="feedback-status"),
                            ]
                        ),
                        id="feedback-form-collapse",
                    ),
                ]
            ),
        ]
    )

#set state varaible that store data in other to acc it globally


app = Dash(__name__,external_stylesheets=[dbc.themes.VAPOR ]) #[dbc.themes.BOOTSTRAP]) #[dbc.themes.SLATE CERULEAN ]))
# store data in session

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.Col(
                            [
                                # toggle button for hidding sidebar
                                daq.ToggleSwitch(
                                    id="toggle-switch",
                                    value=False,
                                    label="Hide/Show Sidebar",
                                    labelPosition="bottom",
                                    color="blue",
                                ),
                            ],
                            width=2,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H1("Sales Pipeline Forcastor"),
                                ],
                                style={"textAlign": "center"},
                            )
                        ),
                    ]
                ),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [   html.Br(),
                        html.Div(dcc.Markdown("*The SuperPixel™ `version 1`*")),
                        dcc.Markdown("---"),
                        html.Div(
                            [sidebar_main()],
                        ),
                        # dbc.Row([drawText()]),
                        # dbc.Row([drawText()]),
                    ],
                    id="column-to-hide",
                    width=4,
                ),
                dbc.Col([body_main()], id="right-column", width=12),
            ],
            align="start",
        ),
        dcc.Store(id='superpixel-data-store'),
        dcc.Store(id='wastedspend-data-store'),
        dcc.Store(id='audiencebuilder-data-store'),
        dcc.Store(id='affiliatelab-data-store'),
    ]
)


# callback for toggleswitch button
@app.callback(
    [Output("column-to-hide", "style"), Output("right-column", "width")],
    Input("toggle-switch", "value"),
)
def toggle_column(toggle_val):
    if not toggle_val:  # If the toggle is off (False)
        return {}, 8  # All columns visible
    return {"display": "none"}, 12  # Middle column hidden, others expanded


# call back to render tabs contens
@app.callback(
    Output("tabs-content-example", "children"), Input("tabs-example", "value")
)
def render_content(tab):
    if tab == "tab-1":
        return html.Div(
            [html.H5("SuperPixel Metrics"), html.Div([])],
            id="superpixel",
        )
    elif tab == "tab-2":
        return html.Div(
            [
                html.H5("Wasted Spend Metrics"),
                html.Hr(),
            ],
            id="wastedspend",
        )
    elif tab == "tab-3":
        return html.Div(
            [
                html.H5("Audience Builder Metrics"),
                html.Hr(),
            ],
            id="audiencebuilder",
        )
    elif tab == "tab-4":
        return html.Div(
            [
                html.H5("AffiliateLab Metrics"),
                html.Hr(),
            ],
            id="affiliatelab",
        )



# call back for dropdown
@app.callback(Output("dropdown-output", "children"), Input("dropdown-menu", "value"))
def update_output(value):
    if value == "SuperPixel":
        return html.Div(
            [
                dcc.Markdown("---"),
                html.H5("SuperPixel Predictor"),
                # Input fields for the SuperPixel function
                dcc.Markdown("---"),
                html.Br(),
                
                dcc.Input(
                    id="Monthly_Traffic",
                    type="number",
                    min=0,
                    placeholder="Enter Monthly Traffic number",
                    style={'width': '92%'}
                ),
                html.Br(),
                dcc.Input(
                    id="Cost_Per_Aquisition",
                    type="number",
                    min=0,
                    placeholder="Enter Cost Per Aquisition number",
                    style={'width': '92%'}
                    
                ),
                html.Br(),
                dcc.Input(
                    id="Deal_Value", 
                    type="number", 
                    min=0, 
                    placeholder="Enter Deal Value",
                    style={'width': '92%'}
                    
                ),
                
                html.Br(),
            
                html.Label("Sales Conversion Rate"),
                dcc.Slider(
                    id="Sales_Conversion_Rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                                
                html.Label("Re-Opt-in Percent"),
                dcc.Slider(
                    id="Re-Opt-in Percent",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Re-Activation Sales Rate"),
                dcc.Slider(
                    id="Re-Activation_Sales_Rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Cost Per Match Re-Activation"),
                dcc.Slider(
                    id="Cost_Per_Match_Re-Activation",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Verification Percent"),
                dcc.Slider(
                    id="Verification_Percent",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("ID Resolution Match Percent"),
                dcc.Slider(
                    id="ID_Resolution_Match_Percent",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                html.Button("Calculate", id="calculate-button"),
            ]
        )

    elif value == "Wasted Spend Metrics":
        return html.Div(
            [
                dcc.Markdown("---"),
                html.H5("Wasted Spend Predictor"),
                dcc.Markdown("---"),
                html.Br(),
                            
                dcc.Input(
                    id="Sales",
                    min=0,
                    type="number",
                    placeholder="Enter Sales value",
                    style={'width': '92%'}
                ),
               
                dcc.Input(
                    id="Price", 
                    type="number", 
                    min=0, 
                    placeholder="Enter price value",
                    style={'width': '92%'}
                ),
                
                dcc.Input(
                    id="Monthly_Traffic",
                    type="number",
                    min=0,
                    placeholder="Enter Monthly Traffic value",
                    style={'width': '92%'}
                ),
                
                dcc.Input(
                    id="Estimated_Spend",
                    type="number",
                    min=0,
                    placeholder="Enter  Estimated Spend value",
                    style={'width': '92%'}
                ),
                html.Br(),
                
                html.Label("Data_Cleaning"),
                dcc.Slider(
                    id="Data_Cleaning",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Pixel Match Rate"),
                dcc.Slider(
                    id="Pixel_Match_Rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Platform Match Rate"),
                dcc.Slider(
                    id="Platform_Match_Rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Sales Conversion Rate"),
                dcc.Slider(
                    id="Sales_Conversion_Rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                html.Button("Calculate", id="calculate_wasted_spend_button"),
                html.Div(id="wasted_spend_output"),
            ]
        )
    elif value == "Audience Builder":
        return html.Div(
            [
                dcc.Markdown("---"),
                html.H5("Audience Builder Predictor"),
                dcc.Markdown("---"),
                html.Br(),
                
                dcc.Input(
                    id="ad-spend-input",
                    min=0,
                    type="number", 
                    placeholder="Enter Ad Spend value",
                    style={'width': '92%'}
                ),
                
                dcc.Input(
                    id="average-order-value-input",
                    type="number",
                    placeholder="Enter average order value",
                    style={'width': '92%'}
                ),
                
                
                dcc.Input(id="cpm-input", 
                          type="number",
                          min=0,
                          placeholder="Enter Cost per 1000 Impressions value",
                          style={'width': '92%'}),
                
                
                html.Br(),
                html.Label("Click Through Rate"),
                dcc.Slider(
                    id="ctr-slider", 
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Site Conversion Rate"),
                dcc.Slider(
                    id="conversion-rate-slider",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                html.Br(),
                # Calculate button
                html.Button("Calculate", id="calculate-button", n_clicks=0),
            ]
        )
    elif value == "AffiliateLab":
        return html.Div(
            [
                # dcc.Markdown("---"),
                html.H5("AffiliateLab Predictor"),
                
                html.Br(),
                          
                dcc.Input(
                    id="your_plan", 
                    placeholder="Your Plan", 
                    type="number", 
                    min=0,
                    style={'width': '92%'}
                ),
                
                
                dcc.Input(
                    id="avg_plan_ref",
                    placeholder="Average Plan Ref",
                    type="number",
                    min=0,
                    style={'width': '92%'}
                ),
                
                html.Label("Sales Conversio Rate"),
                dcc.Slider(
                    id="sales_conversion_rate",
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Response Rate"),
                dcc.Slider(
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                
                html.Label("Ref Payout Percent"),
                dcc.Slider(
                    min=0.0,
                    max=1.0,
                    value=0.05,
                    tooltip=True,
                    marks={i: '' for i in range(1)},
                ),
                html.Button("Calculate", id="calculate-button", n_clicks=0),
            ]
        )


@app.callback(
    Output("feedback-form-collapse", "is_open"),
    [Input("toggle-feedback", "n_clicks")],
    [State("feedback-form-collapse", "is_open")],
)
def toggle_feedback_form(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [
        Output("feedback-text", "value"),
        Output("feedback-status", "children"),
        Output("user-name", "value"),
        Output("user-email", "value"),
    ],
    [Input("submit-button", "n_clicks")],
    [
        State("user-name", "value"),
        State("user-email", "value"),
        State("feedback-text", "value"),
    ],
)
def submit_feedback(n_clicks, user_name, user_email, feedback_text):
    if n_clicks > 0 and feedback_text and user_name and user_email:
        message = send_email(user_email, user_name, feedback_text)
        return "", message, "", ""  # Clear all input fields and display the message
    return feedback_text, None, user_name, user_email


@app.callback(
    [Output("superpixel", "children"), Output("superpixel-data-store", "data")],
    [Input("calculate-button", "n_clicks")],
    [
        # State decorators to fetch current values from input fields
        State("Monthly_Traffic", "value"),
        State("Cost_Per_Aquisition", "value"),
        State("Deal_Value", "value"),
        State("Sales_Conversion_Rate", "value"),
        State("Re-Activation_Sales_Rate", "value"),
        State("Re-Opt-in Percent", "value"),
        State("Cost_Per_Match_Re-Activation", "value"),
        State("Verification_Percent", "value"),
        State("ID_Resolution_Match_Percent", "value"),
    ],
)
def update_calculation(
    n_clicks,
    Monthly_Traffic,
    Cost_Per_Aquisition,
    Sales_Conversion_Rate,
    Deal_Value,
    Re_opt_in_percent,
    Re_activation_Sales_Rate,
    Cost_Per_Match_Re_activation,
    Verification_percent,
    ID_Resolution_Match_percent,
):
    if n_clicks is None:
        return []

    results = SuperPixel(
        Monthly_Traffic,
        Cost_Per_Aquisition,
        Sales_Conversion_Rate,
        Deal_Value,
        Re_opt_in_percent,
        Re_activation_Sales_Rate,
        Cost_Per_Match_Re_activation,
        Verification_percent,
        ID_Resolution_Match_percent,
    )
    
    df = pd.DataFrame(list(results.items()), columns=["Metrics", "Value"])
   
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Recovered Leads']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Recovered Leads</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "100%", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['CPA(After)'])}</h2>"
                                        + f'<p style="font-weight: bold;">CPA(After)</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "100%", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Recovered Revenue'])}</h2>"
                                        + f'<p style="font-weight: bold;">Recovered Revenue</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "100%", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Estimated Spend'])}</h2>"
                                        + f'<p style="font-weight: bold;">Estimated Spend</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "92%", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                ]
            ),
            html.Hr(),
            dbc.Button(
                "Show/Hide Data",
                id="collapse-button",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            generate_table(df),
                            html.Br(),
                            html.A(
                                "Download Data",
                                id="download-link",
                                download="data.csv",
                                href="",
                                target="_blank",
                                className="btn btn-primary",
                            ),
                        ]
                    )
                ),
                id="collapse",
            ),
        ]
    ), df.to_json(date_format='iso', orient='split')


# callback for colapse table button
@app.callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    [State("collapse", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# callback for download link
@app.callback(
    Output("download-link", "href"), 
    [Input("download-link", "n_clicks"), Input("superpixel-data-store", "data")])

def update_download_link(n_clicks, stored_data):
    if n_clicks and stored_data:
        df = pd.read_json(stored_data, orient='split')
        csv_string = df.to_csv(index=False, encoding="utf-8")
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    return None


# collback for wasted spend
@app.callback(
    [Output("wastedspend", "children"),Output("wastedspend-data-store", "data")],
    [Input("calculate_wasted_spend_button", "n_clicks")],
    [
        # State decorators to fetch current values from input fields
        State("Sales", "value"),
        State("Data_Cleaning", "value"),
        State("Estimated_Spend", "value"),
        State("Pixel_Match_Rate", "value"),
        State("Platform_Match_Rate", "value"),
        State("Monthly_Traffic", "value"),
        State("Sales_Conversion_Rate", "value"),
        State("Price", "value"),
    ],
)
def update_wasted_spend_calculation(
    n_clicks,
    Sales,
    Data_Cleaning,
    Estimated_Spend,
    Pixel_Match_Rate,
    Platform_Match_Rate,
    Monthly_Traffic,
    Sales_Conversion_Rate,
    Price,
):
    if n_clicks is None:
        return []

    results = WastedSpend(
        Sales,
        Data_Cleaning,
        Estimated_Spend,
        Pixel_Match_Rate,
        Platform_Match_Rate,
        Monthly_Traffic,
        Sales_Conversion_Rate,
        Price,
    )

    df = pd.DataFrame(list(results.items()), columns=["Metrics", "Value"])
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Lost_Traffic_Total']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Lost Traffic Total</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Wasted_Spend'])}</h2>"
                                        + f'<p style="font-weight: bold;">Wasted Spend</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Revenue'])}</h2>"
                                        + f'<p style="font-weight: bold;">Revenue</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Profit'])}</h2>"
                                        + f'<p style="font-weight: bold;">Profit</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                ]
            ),
            html.Hr(),
            dbc.Button(
                "Show/Hide Data",
                id="collapse-button2",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            generate_table(df),
                            html.Br(),
                            html.A(
                                "Download Data",
                                id="download-link2",
                                download="data.csv",
                                href="",
                                target="_blank",
                                className="btn btn-primary",
                            ),
                        ]
                    )
                ),
                id="collapse2",
            ),
        ]
    ), df.to_json(date_format='iso', orient='split')


# callback for colapse table button
@app.callback(
    Output("collapse2", "is_open"),
    Input("collapse-button2", "n_clicks"),
    [State("collapse2", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# callback for download link
@app.callback(
    Output("download-link2", "href"), 
    [Input("download-link2", "n_clicks"), Input("wastedspend-data-store", "data")])

def update_download_link(n_clicks, stored_data):
    if n_clicks and stored_data:
        df = pd.read_json(stored_data, orient='split')
        csv_string = df.to_csv(index=False, encoding="utf-8")
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    return None

# Define callback to update metrics
@app.callback(
    [Output("audiencebuilder", "children"),Output("audiencebuilder-data-store", "data")],
    [Input("calculate-button", "n_clicks")],
    [
        Input("ad-spend-input", "value"),
        Input("average-order-value-input", "value"),
        Input("cpm-input", "value"),
        Input("ctr-slider", "value"),
        Input("conversion-rate-slider", "value"),
    ],
)
def update_metrics(
    n_clicks, ad_spend, avg_order_value, cpm, ctr_value, conversion_rate_value
):
    if n_clicks == 0:
        return []

    results = AudienceBuilder(
        Ad_Spend=ad_spend,
        Average_Order_Value=avg_order_value,
        Cost_per_1000_Impressions=cpm,
        Click_Through_Rate=ctr_value,
        Site_Conversion_Rate=conversion_rate_value,
    )

    df = pd.DataFrame(list(results.items()), columns=["Metrics", "Value"])
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Clicks']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Clicks</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Cost_per_1_Impression'])}</h2>"
                                        + f'<p style="font-weight: bold;">Cost per 1-Impression</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Total_Profit_After_Adspend'])}</h2>"
                                        + f'<p style="font-weight: bold;">Total Profit After Adspend</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Impressions_Needed']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Impressions Needed</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                ]
            ),
            html.Hr(),
            dbc.Button(
                "Show/Hide Data",
                id="collapse-button3",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            generate_table(df),
                            html.Br(),
                            html.A(
                                "Download Data",
                                id="download-link3",
                                download="data.csv",
                                href="",
                                target="_blank",
                                className="btn btn-primary",
                            ),
                        ]
                    )
                ),
                id="collapse3",
            ),
        ]
    ), df.to_json(date_format='iso', orient='split')


# callback for colapse table button
@app.callback(
    Output("collapse3", "is_open"),
    Input("collapse-button3", "n_clicks"),
    [State("collapse3", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# callback for download link
@app.callback(
    Output("download-link3", "href"), 
    [Input("download-link3", "n_clicks"), Input("audiencebuilder-data-store", "data")])

def update_download_link(n_clicks, stored_data):
    if n_clicks and stored_data:
        df = pd.read_json(stored_data, orient='split')
        csv_string = df.to_csv(index=False, encoding="utf-8")
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    return None


# Define callback to update affiliatelab metrics
@app.callback(
    [Output("affiliatelab", "children"), Output("affiliatelab-data-store", "data")],
    Input("calculate-button", "n_clicks"),
    Input("your_plan", "value"),
    Input("avg_plan_ref", "value"),
    Input("sales_conversion_rate", "value"),
    Input("response_rate", "value"),
    Input("ref_payout_percent", "value"),
)
def update_function(
    n_clicks,
    Your_Plan,
    Avg_Plan_Ref,
    Sales_Conversion_Rate,
    Response_Rate,
    Ref_Payout_Percent,
):
    if n_clicks == 0:
        return []

    results = AffiliateLab(
        Your_Plan,
        Avg_Plan_Ref,
        Sales_Conversion_Rate,
        Response_Rate,
        Ref_Payout_Percent,
    )

    df = pd.DataFrame(list(results.items()), columns=["Metrics", "Value"])
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Touch_Points_Needed']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Touch Points Needed</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Conversations_Needed']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Conversations Needed</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{results['Referrals_Needed_to_Be']:.0f}</h2>"
                                        + f'<p style="font-weight: bold;">Referrals Needed to Be</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    InnerHTML(
                                        '<div class="d-flex flex-column justify-content-center align-items-center h-100">'
                                        + f"<h2>{format_number(results['Payout'])}</h2>"
                                        + f'<p style="font-weight: bold;">Payout</p>'
                                        + "</div>"
                                    )
                                ],
                                className="d-flex",
                            ),
                            style={"height": "90px", "textAlign": "center"},
                            className="mb-2",
                        )
                    ),
                ]
            ),
            html.Hr(),
            dbc.Button(
                "Show/Hide Data",
                id="collapse-button4",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            generate_table(df),
                            html.Br(),
                            html.A(
                                "Download Data",
                                id="download-link4",
                                download="data.csv",
                                href="",
                                target="_blank",
                                className="btn btn-primary",
                            ),
                        ]
                    )
                ),
                id="collapse4",
            ),
        ]
    ), df.to_json(date_format='iso', orient='split')


# callback for colapse table button
@app.callback(
    Output("collapse4", "is_open"),
    Input("collapse-button4", "n_clicks"),
    [State("collapse4", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# callback for download link
@app.callback(
    Output("download-link4", "href"), 
    [Input("download-link4", "n_clicks"), Input("affiliatelab-data-store", "data")])

def update_download_link(n_clicks, stored_data):
    if n_clicks and stored_data:
        df = pd.read_json(stored_data, orient='split')
        csv_string = df.to_csv(index=False, encoding="utf-8")
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    return None


# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.run_server(debug=False)