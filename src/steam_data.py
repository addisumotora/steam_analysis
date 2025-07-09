import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
import random

def get_steam_followers_history(appid):
    url = f"https://steamdb.info/app/{appid}/graphs/"
    
    # browser headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://steamdb.info/',
        'DNT': '1',
    }
    
    try:
        # Add random delay to avoid detection
        time.sleep(random.uniform(1.0, 3.0))
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Check if we got blocked
        if "Access denied" in response.text:
            raise Exception("SteamDB blocked the request. Try again later or use a proxy.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # More robust script finding
        script = None
        for s in soup.find_all('script'):
            if 'followersChart' in s.text:
                script = s
                break
        
        if not script:
            raise Exception("Could not find followersChart script in SteamDB response")
        
        # Extract JSON data from JavaScript
        match = re.search(r'data:\s*(\[.+?\])', script.string)
        if match:
            data_raw = match.group(1)
            # Convert to valid JSON
            data_json = json.loads(data_raw)
            return {
                datetime.utcfromtimestamp(item[0]).strftime('%Y-%m-%d'): item[1] 
                for item in data_json
            }
        return {}
    except Exception as e:
        print(f"SteamDB Error: {e}")
        return {}