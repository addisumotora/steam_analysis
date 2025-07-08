# reddit_collector.py
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from config.config import GAME_NAME, DATE_RANGE_DAYS, OUTPUT_DIR

def get_reddit_mentions():
    """Collect Reddit posts mentioning the game"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=DATE_RANGE_DAYS)
    
    # Convert dates to Unix timestamps
    after = int(start_date.timestamp())
    before = int(end_date.timestamp())
    
    # Corrected endpoint and query structure
    base_url = "https://api.pushshift.io/reddit/submission/search/ "
    params = {
        "q": f"title:{GAME_NAME}",  # Focus on title matches
        "sort": "desc",
        "sort_type": "created_utc",
        "after": after,
        "before": before,
        "size": 100
    }
    
    print(f"Fetching Reddit mentions for '{GAME_NAME}' between {start_date} and {end_date}")
    
    try:
        # Add retry logic
        for attempt in range(3):
            response = requests.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                break
            print(f"Retrying... Attempt {attempt+1}")
            time.sleep(3)
        else:
            raise Exception("Reddit API request failed after 3 retries")
        
        data = response.json().get('data', [])
        if not data:
            print("⚠️ No Reddit mentions found for this time range.")
            return pd.DataFrame(columns=['Date', 'Mentions'])
        
        # Process results
        mentions = []
        for post in data:
            created_utc = datetime.utcfromtimestamp(post['created_utc'])
            mentions.append({
                "Date": created_utc.strftime("%Y-%m-%d"),
                "Mentions": 1
            })
        
        # Aggregate mentions
        df = pd.DataFrame(mentions)
        daily_mentions = df.groupby('Date').size().reset_index(name='Mentions')
        daily_mentions.to_csv(f"{OUTPUT_DIR}/mentions_data.csv", index=False)
        print(f"✅ Saved Reddit mentions to {OUTPUT_DIR}/mentions_data.csv")
        return daily_mentions
    
    except Exception as e:
        print(f"Reddit collection failed: {str(e)}")
        return pd.DataFrame(columns=['Date', 'Mentions'])