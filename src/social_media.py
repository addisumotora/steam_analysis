import praw
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_reddit_mentions(game_name):
    try:
        # Get credentials
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        
        # Validate credentials
        if not client_id or not client_secret:
            logger.error("Missing Reddit API credentials. Check your .env file")
            return {}
        
        logger.info("Authenticating with Reddit API...")
        
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="steam_analytics/1.0",
            check_for_async=False
        )
        # For read-only access, do not check user.me()
        logger.info("Reddit API client initialized in read-only mode.")
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        results = {}
        
        logger.info(f"Searching Reddit for mentions of: {game_name}")
        
        # Search with error handling
        try:
            search_results = reddit.subreddit("all").search(
                query=game_name,
                time_filter="month",
                limit=1000
            )
            
            for submission in search_results:
                try:
                    post_date = datetime.utcfromtimestamp(submission.created_utc).date()
                    if start_date.date() <= post_date <= end_date.date():
                        results[post_date] = results.get(post_date, 0) + 1
                except Exception as e:
                    logger.warning(f"Error processing submission: {e}")
                    
            logger.info(f"Found {len(results)} days with mentions")
            return results
            
        except praw.exceptions.PRAWException as e:
            logger.error(f"Reddit search error: {e}")
            return {}
            
    except Exception as e:
        logger.error(f"Reddit API error: {e}")
        return {}