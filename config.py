import os
from dotenv import load_dotenv
load_dotenv()

# Steam Configuration
APP_ID = 730  # Counter-Strike 2 (example)
GAME_NAME = "Counter-Strike 2"

# Social Media Configuration
SOCIAL_MEDIA = 'reddit'  # Options: reddit, twitter, youtube
DAYS_BACK = 30  

# Output Settings
CSV_FILENAME = 'data/results.csv'
PLOT_FILENAME = 'data/results.png'

# Reddit API credentials from .env
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')