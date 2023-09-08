import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import yagmail
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader




# Function to send emails
def send_email(to_email, subject, Message_body):
    # function to send email to user
    sender_email = "tertimothy@gmail.com"
    receiver_email = to_email
    app_password = "ikilyacpasuvfcgg"  # Replace with your generated App Password

    try:
        # Send email using yagmail
        yag = yagmail.SMTP(sender_email, app_password)
        subject = subject
        message = Message_body
        yag.send(to=receiver_email, subject=subject, contents=message)
        yag.close()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error("check your network or try again later!.")
    return


#function to formmat number 
def format_number(number):
    if isinstance(number, (int, float)):
        if abs(number) < 1000:
            return f"${number:.1f}"
        elif abs(number) < 1e6:
            formatted = number / 1e3
            return f"${formatted:.1f}k"
        elif abs(number) < 1e9:
            formatted = number / 1e6
            return f"${formatted:.1f}M"
        elif abs(number) < 1e12:
            formatted = number / 1e9
            return f"${formatted:.1f}B"
        elif abs(number) < 1e15:
            formatted = number / 1e12
            return f"${formatted:.1f}Trillion"
        else:
            return str(number)
    else:
        return "Invalid input"
    # Define the SuperPixel function



    
# Streamlit app

st.set_page_config(page_title="SuperPixel Calculator", layout="wide",initial_sidebar_state='expanded')
st.title("Sales PipeLine Dasboard")
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
with open(r"C:\Users\USER\Desktop\SalesPipeLine_app\.streamlit\config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#create loging page
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    

#validate

    st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200,use_column_width=True, output_format="PNG")
    
    st.sidebar.title('The SuperPixel™ `version 1`')


    # Create the tabs
    tab1, tab2,tab3, tab4=st.tabs(["SuperPixel", "Wasted Spend Calculator", "Audience Builder", "AffiliateLab"])
    # Sidebar option to select the tab
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Select Tab")

    selected_tab = st.sidebar.selectbox("", ["SuperPixel", "Wasted Spend Calculator", "Audience Builder", "AffiliateLab"])

    if selected_tab == "SuperPixel":
        # Add content to each tab
        with tab1:
            
            
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
                    "CPA(After)": CPA_After}
                
                return calculated_values
                

            # Input parameters inside a st.expander
            with st.sidebar.expander("Input SuperPixel Parameters"):
                Monthly_Traffic = st.number_input("Monthly Traffic:", min_value=0)
                Cost_Per_Aquisition = st.number_input("Cost Per Acquisition:", min_value=0)
                Deal_Value = st.number_input("Deal Value:", min_value=0)
                Sales_Conversion_Rate = st.slider("Sales Conversion Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Re_opt_in_percent = st.slider("Re-Opt-in Percent:", min_value=0.0, max_value=1.0, step=0.01)
                Re_activation_Sales_Rate = st.slider("Re-Activation Sales Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Cost_Per_Match_Re_activation = st.slider("Cost Per Match Re-Activation:", min_value=0)
                Verification_percent = st.slider("Verification Percent:", min_value=0.0, max_value=1.0, step=0.01)
                ID_Resolution_Match_percent = st.slider("ID Resolution Match Percent:", min_value=0.0, max_value=1.0, step=0.01)

            # Calculate button on the sidebar
            if st.sidebar.button("Predict SuperPixel"):
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
            
                st.markdown('## SuperPixel Metrics')
                col1, col2, col3 = st.columns(3)
                
                # Apply the CSS class to metric card elements
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="css-1r6slb0">' +
                        f'<h2>{format_number(calculated_values["Revenue"])}</h2>' +
                        '<p style="font-weight: bold;">Revenue</p>' +
                        '</div>', unsafe_allow_html=True)

                with col2:
                        st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{format_number(calculated_values["Sales"])}</h2>' +
                            '<p style="font-weight: bold;">Sales</p>' +
                            '</div>', unsafe_allow_html=True)

                with col3:
                        st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{format_number(calculated_values["CPA(After)"])}</h2>' +
                            '<p style="font-weight: bold;">CPA After</p>' +
                            '</div>', unsafe_allow_html=True)
                        
                # Display calculated values as metric cards
                st.write('---')
                

                # Display calculated values in a table using a st.expander
                with st.expander("Calculated Values Table"):
                    calculated_values["Timestamp"] = datetime.now()
                    calculated_values_df = pd.DataFrame(calculated_values.items(), columns=["Metric", "Value"])
                    st.dataframe(calculated_values_df, use_container_width=True, hide_index=True, column_config={
                        "Revenue": st.column_config.NumberColumn(
                            "Revenue (in USD)",
                            help="The Revenue of the product in USD",
                            min_value=0,
                            max_value=1000,
                            step=1,
                            format="$%d",
                        )
                    })

                # Download button for calculated values
                csv_download = st.download_button("Download SuperPixel as CSV", calculated_values_df.to_csv(index=False), file_name="calculated_values.csv", mime="text/csv")


        # Wasted Spend Calculator tab
    elif selected_tab == "Wasted Spend Calculator":
        with tab2:
            def WastedSpend(Sales, Data_Cleaning, Estimated_Spend, Pixel_Match_Rate, Platform_Match_Rate, Monthly_traffic, Sales_Conversion_Rate, Price):
                profiles_FB_Google_Pixel_Captured = Monthly_Traffic * 0.15
                Revenue = Price * Sales
                Profit = Revenue - Sales
                Wasted_Spend = Estimated_Spend * 0.75
                Lost_Traffic_Total = Monthly_Traffic - (Monthly_Traffic * Sales_Conversion_Rate)
                Matched_Visitors = Pixel_Match_Rate * Lost_Traffic_Total
                Contactable_Leads = Data_Cleaning * Matched_Visitors
                Targetable_Pixeled_Audience = Platform_Match_Rate * Matched_Visitors

                wasted_spend_values= {
                    "profiles_FB_Google_Pixel_Captured": profiles_FB_Google_Pixel_Captured,
                    "Revenue": Revenue,
                    "Profit": Profit,
                    "Wasted_Spend": Wasted_Spend,
                    "Lost_Traffic_Total": Lost_Traffic_Total,
                    "Matched_Visitors": Matched_Visitors,
                    "Contactable_Leads": Contactable_Leads,
                    "Targetable_Pixeled_Audience": Targetable_Pixeled_Audience
                }
                return wasted_spend_values
            # Input parameters inside a st.expander
            with st.sidebar.expander("Input WastedSpend Parameters"):
                Sales = st.number_input("Sales:", min_value=0)
                Price = st.number_input("Price:", min_value=0)
                Monthly_Traffic = st.number_input("Monthly traffic:", min_value=0)
                Estimated_Spend = st.number_input("Estimated Spend:", min_value=0)
                Data_Cleaning = st.slider("Data Cleaning:", min_value=0.0, max_value=1.0, step=0.01)
                Pixel_Match_Rate = st.slider("Pixel Match Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Platform_Match_Rate = st.slider("Platform Match Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Sales_Conversion_Rate = st.slider("Sales conversion rate:", min_value=0.0, max_value=1.0, step=0.01)
            

            # Calculate button on the sidebar
            if st.sidebar.button("Predict Wasted Spend"):
                wasted_spend_values = WastedSpend(
                    Sales, Data_Cleaning, Estimated_Spend, Pixel_Match_Rate, Platform_Match_Rate,
                    Monthly_Traffic, Sales_Conversion_Rate, Price
                )

                # Display calculated wasted spend values
                st.markdown('## Wasted Spend Metrics')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="css-1r6slb0">' +
                            f'<h2>{format_number(wasted_spend_values["Wasted_Spend"])}</h2>' +
                            '<p style="font-weight: bold;">Wasted Spend</p>' +
                            '</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(wasted_spend_values["Lost_Traffic_Total"])}</h2>' +
                                '<p style="font-weight: bold;">Lost Traffic Total</p>' +
                                '</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(wasted_spend_values["Matched_Visitors"])}</h2>' +
                                '<p style="font-weight: bold;">Matched Visitors</p>' +
                                '</div>', unsafe_allow_html=True)

                        # Display calculated values as metric cards
                st.write('---')

                # Display calculated values in a table using a st.expander
                with st.expander("Calculated Values Table"):
                    wasted_spend_values["Timestamp"] = datetime.now()
                    wasted_spend_values_df = pd.DataFrame(wasted_spend_values.items(), columns=["Metric", "Value"])
                    st.dataframe(wasted_spend_values_df, use_container_width=True, hide_index=True)

                    # Download button for calculated values
                    csv_download = st.download_button("Download Wasted Spend Values as CSV", wasted_spend_values_df.to_csv(index=False), file_name="wasted_spend_values.csv", mime="text/csv")

                # Audience Builder tab
    elif selected_tab == "Audience Builder":
        with tab3:
            #Define the AudienceBuilder function
            def AudienceBuilder(Ad_Spend, Average_Order_Value, Cost_per_1000_Impressions, Click_Through_Rate, Site_Conversion_Rate):
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
                    "Cost_per_1_Impression": Cost_per_1_Impression
                }

                return audience_values

            # Input parameters inside a st.expander
            with st.sidebar.expander("Input Auddience Builder Parameters"):
                Ad_Spend = st.number_input("Ad Spend:", min_value=0)
                Average_Order_Value = st.number_input("Average Order Value:", min_value=0)
                Cost_per_1000_Impressions = st.number_input("Cost per 1000 Impressions:", min_value=0)
                Click_Through_Rate = st.slider("Click Through Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Site_Conversion_Rate = st.slider("Site Conversion Rate:", min_value=0.0, max_value=1.0, step=0.01)

            # Calculate button on the sidebar
            if st.sidebar.button("Predict Audience"):
                audience_values = AudienceBuilder(
                    Ad_Spend, Average_Order_Value, Cost_per_1000_Impressions, Click_Through_Rate, Site_Conversion_Rate
                )

                # Display calculated audience values
                st.markdown('## Audience Metrics')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(audience_values["Impressions_Needed"])}</h2>' +
                                '<p style="font-weight: bold;">Impressions Needed</p>' +
                                '</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(audience_values["Clicks"])}</h2>' +
                                '<p style="font-weight: bold;">Clicks</p>' +
                                '</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(audience_values["CPA"])}</h2>' +
                                '<p style="font-weight: bold;">CPA</p>' +
                                '</div>', unsafe_allow_html=True)

                    # Display calculated values as metric cards
                st.write('---')
                        

                    # Display calculated values in a table using a st.expander
                with st.expander("Calculated Values Table"):
                    audience_values["Timestamp"] = datetime.now()
                    audience_values_df = pd.DataFrame(audience_values.items(), columns=["Metric", "Value"])
                    st.dataframe(audience_values_df, use_container_width=True, hide_index=True)

                    # Download button for calculated values
                    csv_download = st.download_button("Download audience Values as CSV", audience_values_df.to_csv(index=False), file_name="audience_values.csv", mime="text/csv")

    elif selected_tab == "AffiliateLab":
        # AffiliateLab tab
        with tab4:
            def AffiliateLab(Your_Plan, Avg_Plan_Ref, Sales_Conversion_Rate, Response_Rate, Ref_Payout_Percent):
                    Payout = Ref_Payout_Percent * Avg_Plan_Ref
                    Referrals_Needed_to_Be = Your_Plan * Payout
                    Conversations_Needed = Referrals_Needed_to_Be * Sales_Conversion_Rate
                    Touch_Points_Needed = Conversations_Needed * Response_Rate

                    Affiliate_values = {
                        "Payout": Payout,
                        "Referrals_Needed_to_Be": Referrals_Needed_to_Be,
                        "Conversations_Needed": Conversations_Needed,
                        "Touch_Points_Needed": Touch_Points_Needed
                    }
                    return Affiliate_values
            
            # Input parameters inside a st.expander
            with st.sidebar.expander("Input Affiliate Lab Parameters"):
                Your_Plan = st.number_input("Your Plan:", min_value=0)
                Avg_Plan_Ref = st.number_input("Average Plan Referrals:", min_value=0)
                Sales_Conversion_Rate_Aff = st.slider("Sales Conversion Rate (Affiliate):", min_value=0.0, max_value=1.0, step=0.01)
                Response_Rate = st.slider("Response Rate:", min_value=0.0, max_value=1.0, step=0.01)
                Ref_Payout_Percent = st.slider("Referral Payout Percent:", min_value=0.0, max_value=1.0, step=0.01)

            # Calculate button on the sidebar
            if st.sidebar.button("Predict Affiliate Lab"):
                affiliate_values = AffiliateLab(
                    Your_Plan, Avg_Plan_Ref, Sales_Conversion_Rate_Aff, Response_Rate, Ref_Payout_Percent
                )

                # Display calculated affiliate values
                st.markdown('## Affiliate Lab Metrics')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(affiliate_values["Payout"])}</h2>' +
                                '<p style="font-weight: bold;">Payout</p>' +
                                '</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(affiliate_values["Referrals_Needed_to_Be"])}</h2>' +
                                '<p style="font-weight: bold;">Referrals Needed to Be</p>' +
                                '</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="css-1r6slb0">' +
                                f'<h2>{format_number(affiliate_values["Conversations_Needed"])}</h2>' +
                                '<p style="font-weight: bold;">Conversations Needed</p>' +
                                '</div>', unsafe_allow_html=True)

                        # Display calculated values as metric cards
                st.write('---')

                # Display calculated values in a table using a st.expander
                with st.expander("Affilliate Values Table"):
                    affiliate_values["Timestamp"] = datetime.now()
                    affiliate_values_df = pd.DataFrame(affiliate_values.items(), columns=["Metric", "Value"])
                    st.dataframe(affiliate_values_df, use_container_width=True, hide_index=True)

                    # Download button for calculated values
                    csv_download = st.download_button("Download Affiliate Lab Values as CSV", affiliate_values_df.to_csv(index=False), file_name="affiliate_values.csv", mime="text/csv") 
#Change your pass word
if authentication_status:
    try:
        if authenticator.reset_password(username, "Change password", "sidebar"):
            st.sidebar.success("Password Changed successfully")                   
    except Exception as e:
        st.error(e)   
        
    #Add contact information
    with st.expander('Contact Us!'):
        with st.form('your feedbacks', clear_on_submit=True):
            FullName=st.text_input('Name:',help='write your full names')
            email=st.text_input('email:',help='your contact email here')
            Comments=st.text_area('comments:',help='write your comments')
            submitted = st.form_submit_button('Submit')

            if submitted:
                # Random password to be transferred to user securely
                send_email(to_email=email,
                   subject="User Feedback",
                   Message_body= f"Name: {FullName}\nemail: {email}\n {Comments}")
                
                
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
#reset password
try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Reset password',"sidebar")
    if username_forgot_pw:
        st.sidebar.success('New password sent securely')
        # Random password to be transferred to user securely
        send_email(to_email=email_forgot_password,
                   subject="Password Reset",
                   Message_body= f"Enter this password: {random_password }\n Then set your new password")
        
    elif username_forgot_pw == False:
        st.error('Username not found')
except Exception as e:
    st.error(e)

with open(r"C:\Users\USER\Desktop\SalesPipeLine_app\.streamlit\config.yaml", 'w') as file:
    yaml.dump(config, file, default_flow_style=False)    
# Register new user
try:
    if authenticator.register_user("Register new user", "sidebar", preauthorization=True):
        st.sidebar.success("User registered successfully! Make sure you keep your password securely. ")
        sender_email = "tertimothy@gmail.com"
        receiver_email = email
        app_password = "ikilyacpasuvfcgg"  # Replace with your generated App Password
        send_email(to_email=email,
                   subject="User Registration",
                   Message_body= f"Thank you {name} for registering  with us, your username is: {username } \n Please Note! this message is auto generated ***DO NOT REPLAY!***\n Best Regards \n DataOp Team!")
        
except Exception as e:
    st.error(e)

with open(r"C:\Users\USER\Desktop\SalesPipeLine_app\.streamlit\config.yaml", 'w') as file:
    yaml.dump(config, file, default_flow_style=False)    


