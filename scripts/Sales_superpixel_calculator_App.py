import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
# from docx import Document

    
# py -m  streamlit run C:\Users\USER\Desktop\StreamlitApps\SalesPipeLine_App.py
# Define the SuperPixel function
def SuperPixel(Monthly_Traffic, Cost_Per_Aquisition, Sales_Conversion_Rate, Deal_Value, Re_opt_in_percent, Re_activation_Sales_Rate, Cost_Per_Match_Re_activation, Verification_percent, ID_Resolution_Match_percent):
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
        "CPA(After)": CPA_After
    }
    return calculated_values


# Streamlit app
def main():
    st.set_page_config(page_title="SuperPixel Calculator", layout="wide", initial_sidebar_state='expanded')
    
    # Add margin to the top of the title
    st.markdown("<h1 style='text-align: center; margin-top: 1em;'>SuperPixel Calculator</h1>", unsafe_allow_html=True)
           
    st.sidebar.markdown("### Input Parameters")
    st.sidebar.markdown("---")
    # Input fields on the sidebar
    Monthly_Traffic = st.sidebar.number_input("Monthly Traffic:", min_value=0)
    Cost_Per_Aquisition = st.sidebar.number_input("Cost Per Acquisition:", min_value=0)
    Sales_Conversion_Rate = st.sidebar.number_input("Sales Conversion Rate:", min_value=0.0, max_value=1.0, step=0.01)
    Deal_Value = st.sidebar.number_input("Deal Value:", min_value=0)
    Re_opt_in_percent = st.sidebar.number_input("Re-Opt-in Percent:", min_value=0.0, max_value=1.0, step=0.01)
    Re_activation_Sales_Rate = st.sidebar.number_input("Re-Activation Sales Rate:", min_value=0.0, max_value=1.0, step=0.01)
    Cost_Per_Match_Re_activation = st.sidebar.number_input("Cost Per Match Re-Activation:", min_value=0)
    Verification_percent = st.sidebar.number_input("Verification Percent:", min_value=0.0, max_value=1.0, step=0.01)
    ID_Resolution_Match_percent = st.sidebar.number_input("ID Resolution Match Percent:", min_value=0.0, max_value=1.0, step=0.01)

    # Calculate button on the sidebar
    if st.sidebar.button("Predict"):
        calculated_values = SuperPixel(
            Monthly_Traffic, Cost_Per_Aquisition, Sales_Conversion_Rate, Deal_Value,
            Re_opt_in_percent, Re_activation_Sales_Rate, Cost_Per_Match_Re_activation,
            Verification_percent, ID_Resolution_Match_percent
        )
        
        # Store the input data and timestamp in a DataFrame
        input_data = {
            "Timestamp": datetime.now(),
            "Monthly_Traffic": Monthly_Traffic,
            "Cost_Per_Aquisition": Cost_Per_Aquisition,
            "Sales_Conversion_Rate": Sales_Conversion_Rate,
            "Deal_Value": Deal_Value,
            "Re_opt_in_percent": Re_opt_in_percent,
            "Re_activation_Sales_Rate": Re_activation_Sales_Rate,
            "Cost_Per_Match_Re_activation": Cost_Per_Match_Re_activation,
            "Verification_percent": Verification_percent,
            "ID_Resolution_Match_percent": ID_Resolution_Match_percent
        }
        input_df = pd.DataFrame([input_data])

        # Append the input data to a CSV file
        input_df.to_csv("input_history.csv", mode="a", header=not st.session_state.csv_file_exists, index=False)
        st.session_state.csv_file_exists = True
        st.markdown('## Metrics')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue", f"${calculated_values['Revenue']:,}")
            st.metric("Sales", f"${calculated_values['Sales']:,}" if 'Sales' in calculated_values else "$0")
            st.metric("Estimated Spend", f"${calculated_values['Estimated Spend']:,}")
        
        with col2:
            st.metric("Recovered Revenue", f"${calculated_values['Recovered Revenue']:,}")
            st.metric("Recovered Sales", f"${calculated_values['Recovered Sales']:,}")
            st.metric("Recovered Leads", calculated_values['Recovered Leads'])
            st.metric("CPA(After)", f"${calculated_values['CPA(After)']:,}.2f")
        
        with col3:
            st.metric("Anonymous Traffic", calculated_values['Anonymous Traffic'])
            st.metric("Verified Matched Profiles", calculated_values['Verified Matched_Profiles'])
            st.metric("Consumer Matches", calculated_values['Consumer Matches'])
        
       # Display calculated values as metric cards
        st.markdown('''
---
Created with ❤️ by [DataOps Team](https://github.com/VBOHq/Python-KPI-Dashboard-Project).
''')
        

        # Display calculated values in a table
        calculated_values["Timestamp"] = datetime.now()  # Add timestamp to calculated values
        calculated_values_df = pd.DataFrame(calculated_values.items(), columns=["Metric", "Value"])
        st.dataframe(calculated_values_df, hide_index=None, column_config={
        "Revenue": st.column_config.NumberColumn(
            "Revenue (in USD)",
            help="The Revenue of the product in USD",
            min_value=0,
            max_value=1000,
            step=1,
            format="$%d",
        )})
        

        # Download button for calculated values
        csv_download = st.download_button("Download Calculated Values as CSV", calculated_values_df.to_csv(index=False), file_name="calculated_values.csv", mime="text/csv")

    # Toggle button to view history data
    show_history = st.sidebar.checkbox("Show History Data")
    if show_history:
        history_df = pd.read_csv("input_history.csv")
        st.sidebar.write("Input History:")
        st.sidebar.dataframe(history_df)

        # Download button for history data
        history_csv_download = st.sidebar.download_button("Download History as CSV", history_df.to_csv(index=False), file_name="input_history.csv", mime="text/csv")

if __name__ == "__main__":
    if "csv_file_exists" not in st.session_state:
        st.session_state.csv_file_exists = False
    main()