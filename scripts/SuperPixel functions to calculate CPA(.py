# ======= SuperPixel functions to calculate CPA(After) =================
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
    
    return CPA_After

#====================Wasted Pend Calculator ===========

def WastedSpend (Sales,Data_Cleaning, Estimated_Spend,Pixel_Match_Rate,Platform_Match_Rate, Monthly_Traffic,Sales_Conversion_Rate, AOV ):
    #AOV =Price, Units=Sales
    profiles_FB_Google_Pixel_Captured=Monthly_Traffic*0.15	
    Revenue=AOV*Sales	
    Profit=Revenue-Sales	
    Wasted_Spend=Estimated_Spend*0.75	
    Lost_Traffic_Total=Monthly_Traffic-(Monthly_Traffic*Sales_Conversion_Rate)	
    Matched_Visitors=Pixel_Match_Rate*Lost_Traffic_Total	
    Contactable_Leads=Data_Cleaning*Matched_Visitors	
    Targetable_Pixeled_Audience=Platform_Match_Rate*Matched_Visitors	
	
###============= Audiences Breakdown (Audience Builder function)

def AudienceBuider (
Ad_Spend,
Average_Order_Value,
Cost_per_1000_Impressions,
Click_Through_Rate,
Site_Conversion_Rate,):
    Clicks=Impressions_Needed*Click_Through_Rate
    Impressions_Needed= (Ad_Spend/Cost_per_1000_Impressions)*1000
    Total_Sales=Site_Conversion_Rate*Clicks
    CPA = Ad_Spend*Total_Sales
    Revenue=(Ad_Spend/CPA)*Average_Order_Value
    Total_Profit_After_Adspend=Revenue-Ad_Spend
    Cost_per_1_Impressions=Cost_per_1000_Impressions/1000
    '''
    To check whether a strategy is better, you need
    Difference=AuidienceBuider1-AudienceBuilder2
    '''

#=============== AudienceLab Partners(Affiliate Program) ============================

def AffiliateLab (
Your_Plan,
Avg_Plan_Ref,
Sales_Conversion_Rate,
Response_Rate,
Ref_Payout_Percent):
    Payout=Ref_Payout_Percent*Avg_Plan_Ref
    Referrals_Needed_to_Be=Your_Plan* Payout
    Conversations_Needed=Referrals_Needed_to_Be*Sales_Conversion_Rate
    Touch_Points_Needed=Conversations_Needed*Response_Rate




	
	