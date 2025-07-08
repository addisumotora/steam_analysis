import pandas as pd
from datetime import timedelta

def merge_data(steam_data, social_data):
    # Convert to DataFrames
    steam_df = pd.DataFrame(
        [(date, count) for date, count in steam_data.items()],
        columns=['Date', 'Steam_Followers']
    )
    social_df = pd.DataFrame(
        [(date, count) for date, count in social_data.items()],
        columns=['Date', 'Social_Mentions']
    )
    
    # Merge and fill gaps
    merged = pd.merge(
        steam_df, 
        social_df, 
        on='Date', 
        how='outer'
    ).sort_values('Date').fillna(0)
    
    return merged