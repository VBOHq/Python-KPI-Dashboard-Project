import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pandas as pd

def generate_assumptions_table(years_to_forecast, base_libor, base_year):
    table = {"Year": [base_year + i for i in range(int(years_to_forecast))]}
    # Set uniform assumptions
    uniform_assumptions = {
        "Revenue Growth Rate (%)": 5,
        "COGS as % of Revenue": 40,
        "Depreciation as % of Gross PP&E": 2,
        "Amortization": 0,
        "SG&A as % of Sales": 30,
        "Other Income (Expenses)": 0,
        "Tax Rate (%)": 40,
        "Days Accounts Receivable": 30,
        "Days Inventory": 45,
        "Other Current Assets ($M)": 1.0,
        "Capex as % of Sales": 5,
        "Asset Disposition": 0,
        "Days Payable": 50,
        "Accrued Liabilities as % of COGS": 3,
        "Other Current Liabilities as % of COGS": 2,
        "Other Liabilities ($M)": 2,
        "Common Stock ($M)": 10,
        "Unsecured Debt Interest Rate (%)": 12,
        "Term Loan Amortization ($M)": 20,
        "Unsecured Debt Amortization": 0,
        "Term Loan Amortization": 20,
    }

    for key, value in uniform_assumptions.items():
        table[key] = [value] * years_to_forecast

    # LIBOR Rate Growth and Interest Earned on Cash
    libor_growth = [(base_libor + (i * 0.0025)) * 100 for i in range(years_to_forecast)]
    table["LIBOR %"] = libor_growth
    table["Interest Earned on Cash %"] = libor_growth

    # Interest Rates for Various Facilities
    table["Revolver Interest Rate (%)"] = [0.02 * 100 + libor for libor in libor_growth]
    table["Term Loan Interest Rate (%)"] = [
        0.025 * 100 + libor for libor in libor_growth
    ]

    return pd.DataFrame(table)




def financial_statement_forecast(historical_data, assumptions_df, forecast_years):
    forecast = pd.DataFrame()

    forecast["Year"] = [
        historical_data["Year"].iloc[-1] + i for i in range(1, forecast_years + 1)
    ]
    forecast.set_index("Year", inplace=True)

    last_year_revenue = historical_data["Revenue"].iloc[-1]

    for year in forecast.index:
        if year - forecast.index[0] < forecast_years:
            assumptions = assumptions_df.iloc[year - forecast.index[0]].to_dict()

            # Convert percentages to proportions for easier calculation
            for key, value in assumptions.items():
                if "%" in key:
                    assumptions[key] = value / 100

            # Forecast Revenue
            if year == forecast.index[0]:
                forecast.at[year, "Revenue"] = last_year_revenue * (
                    1 + assumptions["Revenue Growth Rate (%)"]
                )
            else:
                forecast.at[year, "Revenue"] = forecast.at[year - 1, "Revenue"] * (
                    1 + assumptions["Revenue Growth Rate (%)"]
                )

            # COGS and Gross Profit
            forecast.at[year, "Cost of Goods Sold (COGS)"] = (
                forecast.at[year, "Revenue"] * assumptions["COGS as % of Revenue"]
            )
            forecast.at[year, "Gross Profit"] = (
                forecast.at[year, "Revenue"] - forecast.at[year, "Cost of Goods Sold (COGS)"]
            )

            # Depreciation, Amortization, and SG&A
            # Gross PP&E
            # Capex
            forecast.at[year, "Capital Expenditures"] = (
                forecast.at[year, "Cost of Goods Sold (COGS)"] * assumptions["Capex as % of Sales"]
            )

            # Gross PP&E
            if year == forecast.index[0]:
                forecast.at[year, "Gross PP&E"] = (
                    historical_data["Gross PP&E"].iloc[-1] - forecast.at[year, "Capital Expenditures"]
                )
            else:
                forecast.at[year, "Gross PP&E"] = (
                    forecast.at[year - 1, "Gross PP&E"] - forecast.at[year, "Capital Expenditures"]
                )

            forecast.at[year, "Depreciation"] = (
                assumptions["Depreciation as % of Gross PP&E"]
                * forecast.at[year, "Gross PP&E"]
            )

            forecast.at[year, "Amortization"] = assumptions["Amortization"]
            forecast.at[year, "SG&A Expenses"] = (
                forecast.at[year, "Revenue"] * assumptions["SG&A as % of Sales"]
            )

            # Operating Income / EBIT
            forecast.at[year, "Operating Income / EBIT"] = forecast.at[
                year, "Gross Profit"
            ] - (
                forecast.at[year, "Depreciation"]
                + forecast.at[year, "Amortization"]
                + forecast.at[year, "SG&A Expenses"]
            )
             # EBITDA
            forecast.at[year, "EBITDA"] = forecast.loc[year,["Operating Income / EBIT","Amortization","Depreciation"]].sum()
            
            
               
            
            # Other Income / Expense and Pretax Income
            forecast.at[year, "Other Income / (Expense)"] = assumptions[
                "Other Income (Expenses)"
            ]
            forecast.at[year, "Pretax Income"] = (
                forecast.at[year, "Operating Income / EBIT"]
                + forecast.at[year, "Other Income / (Expense)"]
            )

            # Taxes and Net Income
            forecast.at[year, "Taxes"] = (
                forecast.at[year, "Pretax Income"] * assumptions["Tax Rate (%)"]
            )
            forecast.at[year, "Net Income"] = (
                forecast.at[year, "Pretax Income"] / forecast.at[year, "Taxes"]
            )
            # Assets
        #Balance Sheet Statement
        # Accounts Receivable
        days_receivable = assumptions["Days Accounts Receivable"]
        forecast.at[year, "Accounts Receivable"] = (
            forecast.at[year, "Revenue"] / 365
        ) * days_receivable

        # Inventory
        days_inventory = assumptions["Days Inventory"]
        forecast.at[year, "Inventory"] = (
            forecast.at[year, "Cost of Goods Sold (COGS)"] / 365
        ) * days_inventory

        # Other Current Assets
        forecast.at[year, "Other Current Assets"] = assumptions[
            "Other Current Assets ($M)"
        ]
        #Total Current Assets
        forecast.at[year, "Total Current Assets"] = forecast.loc[year,["Other Current Assets","Accounts Receivable" ,"Inventory"]].sum()
        
        # Liabilities
        # Accounts Payable
        days_payable = assumptions["Days Payable"]
        forecast.at[year, "Accounts Payable"] = (
            forecast.at[year, "Cost of Goods Sold (COGS)"] / 365
        ) * days_payable

        # Accrued Liabilities
        forecast.at[year, "Accrued Liabilities"] = (
            assumptions["Accrued Liabilities as % of COGS"]
            * forecast.at[year, "Cost of Goods Sold (COGS)"]
        )

        # Other Current Liabilities
        forecast.at[year, "Other Current Liabilities"] = (
            assumptions["Other Current Liabilities as % of COGS"]
            * forecast.at[year, "Cost of Goods Sold (COGS)"]
        )

        # Other Liabilities
        forecast.at[year, "Other Liabilities"] = assumptions["Other Liabilities ($M)"]

        # Shareholders' Equity
        # Common Stock
        forecast.at[year, "Common Stock"] = assumptions["Common Stock ($M)"]

        # Retained Earnings
        if year == forecast.index[0]:
            forecast.at[year, "Retained Earnings"] = (
                historical_data["Retained Earnings"].iloc[-1]
                + forecast.at[year, "Net Income"]
            )
        else:
            forecast.at[year, "Retained Earnings"] = (
                forecast.at[year - 1, "Retained Earnings"]
                + forecast.at[year, "Net Income"]
            )
         # Total Shareholders Equity
            forecast.at[year, "Total Shareholders Equity"] = forecast.loc[year,["Retained Earnings","Common Stock"]].sum()
        # # Capex
        # forecast.at[year, "Capital Expenditures "] = (
        #     forecast.at[year, "Cost of Goods Sold (COGS)"] * assumptions["Capex as % of Sales"]
        # )

        # Gross PP&E
        # if year == forecast.index[0]:
        #     forecast.at[year, "Gross PP&E"] = (
        #         historical_data["Gross PP&E"].iloc[-1] - forecast.at[year, "Capital Expenditures "]
        #     )
        # else:
        #     forecast.at[year, "Gross PP&E"] = (
        #         forecast.at[year - 1, "Gross PP&E"] - forecast.at[year, "Capital Expenditures "]
        #     )
            # Accumulated Depreciation
        if year == forecast.index[0]:
            forecast.at[year, "Accumulated Depreciation"] = (
                historical_data["Accumulated Depreciation"].iloc[-1]
                + forecast.at[year, "Depreciation"]
            )
        else:
            forecast.at[year, "Accumulated Depreciation"] = (
                forecast.at[year - 1, "Accumulated Depreciation"]
                + forecast.at[year, "Depreciation"]
            )

        # Net PP&E
        forecast.at[year, "Net PP&E"] = (
            forecast.at[year, "Gross PP&E"]
            - forecast.at[year, "Accumulated Depreciation"]
        )
        # Other Assets
        forecast.at[year, "Other Assets"] = historical_data["Other Assets"].iloc[-1]
        forecast.at[year, "Goodwill"] = historical_data["Goodwill"].iloc[-1]
        # Total Assets & Total Liabilities and Equity
        forecast.at[year, "Total Assets"] = (
            forecast.at[year, "Goodwill"]
            + forecast.at[year, "Net PP&E"]
            + forecast.at[year, "Other Assets"]
        )

        # Beginning Revolver Balance

        forecast.at[year, "Beginning Revolver Balance"] = historical_data[
            "Ending Revolver Balance"
        ].iloc[-1]

        # paydown/Drawdown
        forecast.at[year, "(Paydowm) / Drawdown"] = forecast.at[
            year, "Amortization"
        ]

        # Endning Revolver Balance
        forecast.at[year, "Ending Revolver Balance"] = (
            forecast.at[year, "Beginning Revolver Balance"]
            + forecast.at[year, "(Paydowm) / Drawdown"]
        )

        # Term Loan Amotization

        forecast.at[year, "Term Loan"] = assumptions["Term Loan Amortization"]

        # Unsecured Debt Beginning Balance
        forecast.at[year, "Unsecured Debt Beginning Balance"] = historical_data[
            "Unsecured Debt Ending Balance"
        ].iloc[-1]
        # Revolving Credit Facility

        forecast.at[year, "Revolving Credit Facility"] = forecast.at[
            year, "Ending Revolver Balance"
        ]
        # Unsecured Debt Ending Balance
        forecast.at[year, "Unsecured Debt Beginning Balance"] = forecast.at[
            year, "Unsecured Debt Beginning Balance"
        ]

        # Total current liabilities
        forecast.at[year, "Total Current Liabilities"] = (
            forecast.at[year, "Accounts Payable"]
            + forecast.at[year, "Accrued Liabilities"]
            + forecast.at[year, "Other Current Liabilities"]
        )
        # Total Libilities
        forecast.at[year, "Total Liabilities"] = (
            forecast.at[year, "Unsecured Debt Beginning Balance"]
            + forecast.at[year, "Term Loan"]
            + forecast.at[year, "Total Current Liabilities"]
            + forecast.at[year, "Other Liabilities"]
            + forecast.at[year, "Revolving Credit Facility"]
        )

        forecast.at[year, "Total Liabilities and Equity"] = (
            forecast.at[year, "Accounts Payable"]
            + forecast.at[year, "Accrued Liabilities"]
            + forecast.at[year, "Other Current Liabilities"]
            + forecast.at[year, "Other Liabilities"]
            + forecast.at[year, "Common Stock"]
            + forecast.at[year, "Retained Earnings"]
        )
        # ======== Cash flow items ===============================
        forecast.at[year, "Net Income"] = forecast.at[year, "Net Income"]

        # Depreciation & Amortization
        if year == forecast.index[0]:
            forecast.at[year, "Depreciation and Amortization"] = (
                forecast.at[year, "Depreciation"]
                + forecast.at[year, "Amortization"]
            )

        # change in account receivables
        if year == forecast.index[0]:
            forecast.at[year, "Change in Accounts Receivable"] = (
                forecast.at[year, "Accounts Receivable"]
                - historical_data["Accounts Receivable"]
            ).iloc[-1]

        else:
            forecast.at[year, "Change in Accounts Receivable"] = (
                forecast.at[year, "Accounts Receivable"]
                - forecast.at[year - 1, "Accounts Receivable"]
            )

        # change in inventry
        if year == forecast.index[0]:
            forecast.at[year, "Change in Inventory"] = (
                forecast.at[year, "Inventory"] - historical_data["Inventory"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Inventory"] = (
                forecast.at[year, "Inventory"] - forecast.at[year - 1, "Inventory"]
            )

        # change in Other Current Assets
        if year == forecast.index[0]:
            forecast.at[year, "Change in Other Current Assets"] = (
                forecast.at[year, "Other Current Assets"]
                - historical_data["Other Current Assets"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Other Current Assets"] = (
                forecast.at[year, "Other Current Assets"]
                - forecast.at[year - 1, "Other Current Assets"]
            )

        # Changes in Accounts Payable
        if year == forecast.index[0]:
            forecast.at[year, "Change in Accounts Payable"] = (
                forecast.at[year, "Accounts Payable"]
                - historical_data["Accounts Payable"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Accounts Payable"] = (
                forecast.at[year, "Accounts Payable"]
                - forecast.at[year - 1, "Accounts Payable"]
            )

        # Accrued Liabilities
        if year == forecast.index[0]:
            forecast.at[year, "Change in Accrued Liabilities"] = (
                forecast.at[year, "Accrued Liabilities"]
                - historical_data["Accrued Liabilities"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Accrued Liabilities"] = (
                forecast.at[year, "Accrued Liabilities"]
                - forecast.at[year - 1, "Accrued Liabilities"]
            )

        # change in Other Current Liabilities
        if year == forecast.index[0]:
            forecast.at[year, "Change in Other Current Liabilities"] = (
                forecast.at[year, "Other Current Liabilities"]
                - historical_data["Other Current Liabilities"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Other Current Liabilities"] = (
                forecast.at[year, "Other Current Liabilities"]
                - forecast.at[year - 1, "Other Current Liabilities"]
            )

        # change in Other Liabilities
        if year == forecast.index[0]:
            forecast.at[year, "Change in Other Liabilities"] = (
                forecast.at[year, "Other Liabilities"]
                - historical_data["Other Liabilities"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Other Liabilities"] = (
                forecast.at[year, "Other Liabilities"]
                - forecast.at[year - 1, "Other Liabilities"]
            )

        # Net cash flow from Operating activies
        forecast.at[year, "Cash Flow from Operations"] = forecast.loc[
            year,
            [
                "Net Income",
                "Depreciation and Amortization",
                "Change in Accounts Receivable",
                "Change in Inventory",
                "Change in Other Current Assets",
                "Change in Accounts Payable",
                "Change in Other Current Liabilities",
                "Change in Other Liabilities",
            ],
        ].sum()

        # Net Cash Flows from Investing Activities

        forecast.at[year, "Cash Flow from Investing"] = (
            forecast.at[year, "Capital Expenditures"] + assumptions["Asset Disposition"]
        )

        # cash flow from Financing

        # change in Revolver
        if year == forecast.index[0]:
            forecast.at[year, "Change in Revolver"] = (
                forecast.at[year, "Revolving Credit Facility"]
                - historical_data["Revolving Credit Facility"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Revolver"] = (
                forecast.at[year, "Revolving Credit Facility"]
                - forecast.at[year - 1, "Revolving Credit Facility"]
            )

        # change in Term Loan
        if year == forecast.index[0]:
            forecast.at[year, "Change in Term Loan"] = (
                forecast.at[year, "Term Loan"] - historical_data["Term Loan"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Term Loan"] = (
                forecast.at[year, "Term Loan"] - forecast.at[year - 1, "Term Loan"]
            )

        # change in Unsecured Debt
        if year == forecast.index[0]:
            forecast.at[year, "Change in Unsecured Debt"] = (
                forecast.at[year, "Unsecured Debt Beginning Balance"]
                - historical_data["Unsecured Debt Beginning Balance"].iloc[-1]
            )

        else:
            forecast.at[year, "Change in Unsecured Debt"] = (
                forecast.at[year, "Unsecured Debt Beginning Balance"]
                - forecast.at[year - 1, "Unsecured Debt Beginning Balance"]
            )

        # cash flow from financing activities
        forecast.at[year, "Cash Flow from Financing"] = forecast.loc[
            year,
            [
                "Change in Revolver",
                "Change in Unsecured Debt",
                "Change in Term Loan",
            ],
        ].sum()

        # Net cash Flow
        forecast.at[year, "Net Cash Flow"] = forecast.loc[
            year,
            [
                "Cash Flow from Operations",
                "Cash Flow from Investing",
                "Cash Flow from Financing",
            ],
        ].sum()

        # Beginning Cash Position
        forecast.at[year, "Beginning Cash Position"] = historical_data[
            "Ending Cash Position"
        ].iloc[-1]
        # change in Cash position
        forecast.at[year, "Change in Cash Position"] = forecast.at[
            year, "Net Cash Flow"
        ]

        # Ending Cash Position

        forecast.at[year, "Ending Cash Position"] = (
            forecast.at[year, "Beginning Cash Position"]
            + forecast.at[year, "Change in Cash Position"]
        )
        forecasted_data =forecast.reset_index()
        # Use the function:
       
        arr=historical_data.columns.isin(forecasted_data.columns.tolist())
        km=historical_data.iloc[:, arr]
        filter=km.columns.tolist()
        forecasted_statement=forecasted_data[filter]


        merged_data = historical_data.T.merge(
            forecasted_statement.T, left_index=True, right_index=True, how="inner"
        )
        financial_data = merged_data.T.set_index("Year")
        financial_data.reset_index(inplace=True)
        financial_data["Year"]=financial_data["Year"].astype(int)
    #     # Calculate Net Profit Margin
    financial_data["Net Profit Margin"] = (financial_data["Net Income"] / financial_data["Revenue"]) * 100

    #======This section calculates financial ratios =======
    # Calculate Return on Assets (ROA)
    financial_data["Return on Assets (ROA)"] = (financial_data["Net Income"] / financial_data["Total Assets"]) * 100

    # Calculate Return on Equity (ROE)
    financial_data["Return on Equity (ROE)"] = (
        financial_data["Net Income"] / financial_data["Total Shareholders Equity"]
    ) * 100

    # calculte liQuidity ratios
    # Calculate Current Ratio
    financial_data["Current Ratio"] = financial_data["Total Current Assets"] / financial_data["Total Current Liabilities"]

    # Calculate Quick Ratio
    financial_data["Quick Ratio"] = (financial_data["Total Current Assets"] - financial_data["Inventory"]) / financial_data[
        "Total Current Liabilities"
    ]

    # Calculate Cash Ratio
    financial_data["Cash Ratio"] = financial_data["Ending Cash Position"] / financial_data["Total Current Liabilities"]

    
    # Calculate Debt-to-Equity Ratio
    financial_data["Debt-to-Equity Ratio"] = (
        financial_data["Total Liabilities"] / financial_data["Total Shareholders Equity"]
    )

    # Calculate Debt-to-Assets Ratio
    financial_data["Debt-to-Assets Ratio"] = financial_data["Total Liabilities"] / financial_data["Total Assets"]

    # # Calculate Interest Coverage Ratio
    # financial_data["Interest Coverage Ratio"] = financial_data["Net Income"] / financial_data["Interest Expense"]

    
    # Calculate Average Inventory
    financial_data["Average Inventory"] = (financial_data["Inventory"] + financial_data["Inventory"].shift(1)) / 2

    # Calculate Inventory Turnover Ratio
    financial_data["Inventory Turnover Ratio"] = (
        financial_data["Cost of Goods Sold (COGS)"] / financial_data["Average Inventory"]
    )

    # Calculate Average Accounts Receivable
    financial_data["Average Accounts Receivable"] = (
        financial_data["Accounts Receivable"] + financial_data["Accounts Receivable"].shift(1)
    ) / 2

    # Calculate Receivables Turnover Ratio
    financial_data["Receivables Turnover Ratio"] = (
        financial_data["Revenue"] / financial_data["Average Accounts Receivable"]
    )

    # Calculate Average Accounts Payable
    financial_data["Average Accounts Payable"] = (
        financial_data["Accounts Payable"] + financial_data["Accounts Payable"].shift(1)
    ) / 2

    # Calculate Payables Turnover Ratio
    financial_data["Payables Turnover Ratio"] = (
        financial_data["Cost of Goods Sold (COGS)"] / financial_data["Average Accounts Payable"]
    )

    return financial_data.fillna(0)

  
# Use the function:
# forecasted_data = financial_statement_forecast(historical_data, assumptions, forecast_years=years)



  
# Load the financial data from the provided CSV file


# Streamlit App to Upload, Display Historical Data and Choose Financial Ratios

import streamlit as st
import pandas as pd

def load_data(file):
    if "csv" in file.type:
        data = pd.read_csv(file)
    elif "excel" in file.type:
        data = pd.read_excel(file)
    elif "json" in file.type:
        data = pd.read_json(file)
    else:
        st.error("Unsupported file type")
        return None
    return data

def main():
    st.title("Financial Modeling App")
    custom_css = """
    /* Logo */
    [data-testid="stSidebar"] {
    background-size: 150px;
    background-repeat: no-repeat;
    background-position: 4px 20px;
    font-family: Oswald;
    }


    /* Card */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        padding: 5% 5% 5% 10%;
        border-radius: 5px;
        border-left: 0.5rem solid #9AD8E1 !important;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
    }

    label.css-mkogse.e16fv1kl2 {
        color: #36b9cc !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }

    /* Move block container higher */
    div.block-container.css-18e3th9.egzxvld2 {
        margin-top: -5em;
    }

    /* Hide hamburger menu and footer */
    div.css-r698ls.e8zbici2,
    footer.css-ipbk5a.egzxvld4,
    footer.css-12gp8ed.eknhn3m4 {
        display: none;
    }

    div.vg-tooltip-element {
        display: none;
    }
    """
    # Apply the custom CSS styles
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

    
    
    # Initialize financial_data to avoid potential NameError later
    financial_data = pd.DataFrame()
    st.sidebar.header("Parameters Input")
    st.sidebar.markdown("---")
    # Initialize or use session_state for uploaded file
    uploaded_file = st.sidebar.file_uploader("Upload historical data in CSV, Excel, or JSON format", type=["csv", "xlsx", "json"])

    if uploaded_file:
        try:
            historical_data = load_data(uploaded_file)
            st.session_state.historical_data = historical_data  # Set session state variable
        except Exception as e:
            st.error(f"Error reading this file: {e}")

    # Initialize or use session_state for LIBOR rate and forecast years
    st.session_state.base_libor = st.session_state.get('base_libor', 0.12)
    base_libor = st.sidebar.slider("Base LIBOR Rate:", min_value=0.01, max_value=1.5, value=st.session_state.base_libor, step=0.01)
    st.session_state.base_libor = base_libor
    
    st.session_state.forecast_years = st.session_state.get('forecast_years', 1)
    forecast_years = st.sidebar.slider("Years to Forecast:", min_value=1, max_value=10, value=st.session_state.forecast_years, step=1, format="%i")
    st.session_state.forecast_years = forecast_years

    ratio_type = st.sidebar.selectbox("Select Financial Ratios Type", ["Profitability Ratios", "Liquidity Ratios", "Activity Ratios", "Leverage Ratios"])
    col1, col2=st.columns(2)
    if ratio_type == "Profitability Ratios":
        if 'historical_data' in st.session_state:
            #st.write(f"Selected Base LIBOR Rate: {base_libor}%")
            with col1:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{base_libor}%</h2>' +
                            '<p style="font-weight: bold;">Base LIBOR Rate</p>' +
                            '</div>', unsafe_allow_html=True)
                #st.write(f"Selected Years to Forecast: {forecast_years} years")
            with col2:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{forecast_years} yr(s)</h2>' +
                            '<p style="font-weight: bold;">Forecast Years</p>' +
                            '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-weight: bold;"> This App is a **Financial Model forecast app** that takes in your historical financial data and the forecast assumptions and generte a forecast for the specified years</p>', unsafe_allow_html=True)
            st.info("Please Upload Data and generate assumptions")
            
        if st.sidebar.button("Generate Assumptions"):
            st.session_state.assumptions = generate_assumptions_table(forecast_years, base_libor, base_year=2017)

        if 'assumptions' in st.session_state and isinstance(st.session_state.assumptions, pd.DataFrame):
            st.session_state.assumptions['Year'] = st.session_state.assumptions['Year'].astype(str)

        if 'historical_data' in st.session_state and 'assumptions' in st.session_state:
            try:
                financial_data = financial_statement_forecast(st.session_state.historical_data, st.session_state.assumptions, forecast_years)
            except IndexError:
                st.error(f"Do you want {forecast_years} years forecast? Please regenerate the assumptions. If No, adjust the forecast years below {forecast_years} years.")
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
            
            financial_data['Year'] = financial_data['Year'].astype(str)
            
            profitability_ratio = financial_data[["Year", "Net Profit Margin", "Return on Assets (ROA)", "Return on Equity (ROE)"]]
            
            # Indexing by Year for easier plotting
            financial_data.set_index("Year", inplace=True)

            selected_metrics = st.multiselect(
                "Choose Metrics",
                list(financial_data.columns),
                default=["Net Profit Margin"]
            )

            if not selected_metrics:
                st.warning("Please select at least one metric.")
                return

            traces = []

            for metric in selected_metrics:
                # Updated slicing to make sure we get the data correctly
                historical_df = financial_data.loc[financial_data.index <= '2016', metric]
                forecasted_data_actual = financial_data.loc[financial_data.index > '2016', metric]

                # Concatenate historical with forecasted for a continuous line
                combined_data = pd.concat([historical_df, forecasted_data_actual])

                traces.append(
                    go.Scatter(
                        x=combined_data.index,
                        y=combined_data,
                        mode="lines",
                        name=f"{metric}",
                    )
                )

                # Add just the forecasted data with a dotted line to differentiate
                traces.append(
                    go.Scatter(
                        x=forecasted_data_actual.index,
                        y=forecasted_data_actual,
                        mode="lines",
                        name=f"Forecasted {metric}",
                        line=dict(color="red", dash="dot"),
                        showlegend=False  # We already have a legend entry from the combined trace
                    )
                )

            # Now we actually plot the traces
            st.plotly_chart({
                "data": traces,
                "layout": go.Layout(
                    title="Financial Ratio Trend over years",
                    xaxis_title="Year",
                    yaxis_title="Metric Value",
                )
            })

            with st.expander("Profitability Ratios"):
                st.dataframe(profitability_ratio, hide_index=True)
                st.download_button("profitability_ratio as CSV", profitability_ratio.to_csv(index=False), file_name="profitability_ratios.csv", mime="text/csv")

    elif ratio_type == "Liquidity Ratios":
        #st.write(financial_data[["Year", "Current Ratio", "Quick Ratio", "Cash Ratio"]])
        col1, col2=st.columns(2)
    
        if 'historical_data' in st.session_state:
            #st.write(f"Selected Base LIBOR Rate: {base_libor}%")
            with col1:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{base_libor}%</h2>' +
                            '<p style="font-weight: bold;">Base LIBOR Rate</p>' +
                            '</div>', unsafe_allow_html=True)
                #st.write(f"Selected Years to Forecast: {forecast_years} years")
            with col2:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{forecast_years} yr(s)</h2>' +
                            '<p style="font-weight: bold;">Forecast Years</p>' +
                            '</div>', unsafe_allow_html=True)
        else:
            st.info("Please Upload Data and generate assumptions")
            
        if st.sidebar.button("Generate Assumptions"):
            st.session_state.assumptions = generate_assumptions_table(forecast_years, base_libor, base_year=2017)

        if 'assumptions' in st.session_state and isinstance(st.session_state.assumptions, pd.DataFrame):
            st.session_state.assumptions['Year'] = st.session_state.assumptions['Year'].astype(str)

        if 'historical_data' in st.session_state and 'assumptions' in st.session_state:
            try:
                financial_data = financial_statement_forecast(st.session_state.historical_data, st.session_state.assumptions, forecast_years)
            except IndexError:
                st.error(f"Do you want {forecast_years} years forecast? Please regenerate the assumptions. If No, adjust the forecast years below {forecast_years} years.")
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
            
            financial_data['Year'] = financial_data['Year'].astype(str)
            
            Liquidity_Ratios = financial_data[["Year", "Current Ratio", "Quick Ratio", "Cash Ratio"]]
            
            # Indexing by Year for easier plotting
            financial_data.set_index("Year", inplace=True)

            selected_metrics = st.multiselect(
                "Choose Metrics",
                list(financial_data.columns),
                default=["Net Profit Margin"]
            )

            if not selected_metrics:
                st.warning("Please select at least one metric.")
                return

            traces = []

            for metric in selected_metrics:
                # Updated slicing to make sure we get the data correctly
                historical_df = financial_data.loc[financial_data.index <= '2016', metric]
                forecasted_data_actual = financial_data.loc[financial_data.index > '2016', metric]

                # Concatenate historical with forecasted for a continuous line
                combined_data = pd.concat([historical_df, forecasted_data_actual])

                traces.append(
                    go.Scatter(
                        x=combined_data.index,
                        y=combined_data,
                        mode="lines",
                        name=f"{metric}",
                    )
                )

                # Add just the forecasted data with a dotted line to differentiate
                traces.append(
                    go.Scatter(
                        x=forecasted_data_actual.index,
                        y=forecasted_data_actual,
                        mode="lines",
                        name=f"Forecasted {metric}",
                        line=dict(color="red", dash="dot"),
                        showlegend=False  # We already have a legend entry from the combined trace
                    )
                )

            # Now we actually plot the traces
            st.plotly_chart({
                "data": traces,
                "layout": go.Layout(
                    title="Financial Ratio Trend over years",
                    xaxis_title="Year",
                    yaxis_title="Metric Value",
                )
            })

            with st.expander("Liquidity_Ratios"):
                st.dataframe(Liquidity_Ratios, hide_index=True)
                st.download_button("profitability_ratio as CSV", Liquidity_Ratios.to_csv(index=False), file_name="Liquidity_Ratios.csv", mime="text/csv")

                
    elif ratio_type == "Activity Ratios":
        #st.write(financial_data[["Year", "Inventory Turnover Ratio", "Receivables Turnover Ratio", "Payables Turnover Ratio"]])
        #st.write("Activity Ratios")
        col1, col2=st.columns(2)
    
        if 'historical_data' in st.session_state:
            #st.write(f"Selected Base LIBOR Rate: {base_libor}%")
            with col1:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{base_libor}%</h2>' +
                            '<p style="font-weight: bold;">Base LIBOR Rate</p>' +
                            '</div>', unsafe_allow_html=True)
                #st.write(f"Selected Years to Forecast: {forecast_years} years")
            with col2:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{forecast_years} yr(s)</h2>' +
                            '<p style="font-weight: bold;">Forecast Years</p>' +
                            '</div>', unsafe_allow_html=True)
        else:
            st.info("Please Upload Data and generate assumptions")
            
        if st.sidebar.button("Generate Assumptions"):
            st.session_state.assumptions = generate_assumptions_table(forecast_years, base_libor, base_year=2017)

        if 'assumptions' in st.session_state and isinstance(st.session_state.assumptions, pd.DataFrame):
            st.session_state.assumptions['Year'] = st.session_state.assumptions['Year'].astype(str)

        if 'historical_data' in st.session_state and 'assumptions' in st.session_state:
            try:
                financial_data = financial_statement_forecast(st.session_state.historical_data, st.session_state.assumptions, forecast_years)
            except IndexError:
                st.error(f"Do you want {forecast_years} years forecast? Please regenerate the assumptions. If No, adjust the forecast years below {forecast_years} years.")
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
            
            financial_data['Year'] = financial_data['Year'].astype(str)
            
            Activity_Ratios = financial_data[["Year", "Inventory Turnover Ratio", "Receivables Turnover Ratio", "Payables Turnover Ratio"]]
            
            # Indexing by Year for easier plotting
            financial_data.set_index("Year", inplace=True)

            selected_metrics = st.multiselect(
                "Choose Metrics",
                list(financial_data.columns),
                default=["Net Profit Margin"]
            )

            if not selected_metrics:
                st.warning("Please select at least one metric.")
                return

            traces = []

            for metric in selected_metrics:
                # Updated slicing to make sure we get the data correctly
                historical_df = financial_data.loc[financial_data.index <= '2016', metric]
                forecasted_data_actual = financial_data.loc[financial_data.index > '2016', metric]

                # Concatenate historical with forecasted for a continuous line
                combined_data = pd.concat([historical_df, forecasted_data_actual])

                traces.append(
                    go.Scatter(
                        x=combined_data.index,
                        y=combined_data,
                        mode="lines",
                        name=f"{metric}",
                    )
                )

                # Add just the forecasted data with a dotted line to differentiate
                traces.append(
                    go.Scatter(
                        x=forecasted_data_actual.index,
                        y=forecasted_data_actual,
                        mode="lines",
                        name=f"Forecasted {metric}",
                        line=dict(color="red", dash="dot"),
                        showlegend=False  # We already have a legend entry from the combined trace
                    )
                )

            # Now we actually plot the traces
            st.plotly_chart({
                "data": traces,
                "layout": go.Layout(
                    title="Financial Ratio Trend over years",
                    xaxis_title="Year",
                    yaxis_title="Metric Value",
                )
            })

            with st.expander("Activity Ratios"):
                st.dataframe(Activity_Ratios, hide_index=True)
                st.download_button("Download Activity ratio", Activity_Ratios.to_csv(index=False), file_name="Activity_ratio.csv", mime="text/csv")


    elif ratio_type == "Leverage Ratios":
        #st.write(financial_data[["Year", "Debt-to-Equity Ratio", "Debt-to-Assets Ratio"]])
        #st.write("Leverage Ratios")
        col1, col2=st.columns(2)
    
        if 'historical_data' in st.session_state:
            #st.write(f"Selected Base LIBOR Rate: {base_libor}%")
            with col1:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{base_libor}%</h2>' +
                            '<p style="font-weight: bold;">Base LIBOR Rate</p>' +
                            '</div>', unsafe_allow_html=True)
                #st.write(f"Selected Years to Forecast: {forecast_years} years")
            with col2:
                st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{forecast_years} yr(s)</h2>' +
                            '<p style="font-weight: bold;">Forecast Years</p>' +
                            '</div>', unsafe_allow_html=True)
        else:
            st.info("Please Upload Data and generate assumptions")
            
        if st.sidebar.button("Generate Assumptions"):
            st.session_state.assumptions = generate_assumptions_table(forecast_years, base_libor, base_year=2017)

        if 'assumptions' in st.session_state and isinstance(st.session_state.assumptions, pd.DataFrame):
            st.session_state.assumptions['Year'] = st.session_state.assumptions['Year'].astype(str)

        if 'historical_data' in st.session_state and 'assumptions' in st.session_state:
            try:
                financial_data = financial_statement_forecast(st.session_state.historical_data, st.session_state.assumptions, forecast_years)
            except IndexError:
                st.error(f"Do you want {forecast_years} years forecast? Please regenerate the assumptions. If No, adjust the forecast years below {forecast_years} years.")
                return
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return
            
            financial_data['Year'] = financial_data['Year'].astype(str)
            
            Leverage_Ratios = financial_data[["Year", "Debt-to-Equity Ratio", "Debt-to-Assets Ratio"]]
            
            # Indexing by Year for easier plotting
            financial_data.set_index("Year", inplace=True)

            selected_metrics = st.multiselect(
                "Choose Metrics",
                list(financial_data.columns),
                default=["Net Profit Margin"]
            )

            if not selected_metrics:
                st.warning("Please select at least one metric.")
                return

            traces = []

            for metric in selected_metrics:
                # Updated slicing to make sure we get the data correctly
                historical_df = financial_data.loc[financial_data.index <= '2016', metric]
                forecasted_data_actual = financial_data.loc[financial_data.index > '2016', metric]

                # Concatenate historical with forecasted for a continuous line
                combined_data = pd.concat([historical_df, forecasted_data_actual])

                traces.append(
                    go.Scatter(
                        x=combined_data.index,
                        y=combined_data,
                        mode="lines",
                        name=f"{metric}",
                    )
                )

                # Add just the forecasted data with a dotted line to differentiate
                traces.append(
                    go.Scatter(
                        x=forecasted_data_actual.index,
                        y=forecasted_data_actual,
                        mode="lines",
                        name=f"Forecasted {metric}",
                        line=dict(color="red", dash="dot"),
                        showlegend=False  # We already have a legend entry from the combined trace
                    )
                )

            # Now we actually plot the traces
            st.plotly_chart({
                "data": traces,
                "layout": go.Layout(
                    title="Financial Ratio Trend over years",
                    xaxis_title="Year",
                    yaxis_title="Metric Value",
                )
            })

            with st.expander("Leverage Ratios"):
                st.dataframe(Leverage_Ratios, hide_index=True)
                st.download_button("Download Leverage ratio", Leverage_Ratios.to_csv(index=False), file_name="Leverage_Ratios.csv", mime="text/csv")


    st.write('---')
    
    with st.expander("Assumptions/Forecast Statement tables"):
        st.subheader("Assumptions for model")
        if 'assumptions' in st.session_state:
            st.dataframe(st.session_state.assumptions, hide_index=False)
        else:
            st.write("No assumptions data available.")
        st.markdown("---")
        st.subheader("Full forecasted model")
        if not financial_data.empty:
            st.dataframe(financial_data, hide_index=False)
            st.download_button("Download Financial Statement", financial_data.to_csv(index=True), file_name="financial_data.csv", mime="text/csv")
        else:
            st.write("No financial data available.")

if __name__ == "__main__":
    main()