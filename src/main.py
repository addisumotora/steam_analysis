import os
import sys
import logging
import traceback

# Add parent directory to Python path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import config
from steam_data import get_steam_followers_history
from social_media import get_reddit_mentions
from data_processor import merge_data
from visualizer import plot_results
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('steam_analytics.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info(f"🚀 Starting analytics for {config.GAME_NAME} (AppID: {config.APP_ID})")
        
        # Get Steam data
        logger.info("🔍 Fetching Steam follower history...")
        steam = get_steam_followers_history(config.APP_ID)
        if not steam:
            logger.error("❌ Failed to retrieve Steam data")
        else:
            logger.info(f"✅ Retrieved Steam data: {len(steam)} records")
        
        # Get Social media data
        logger.info("📱 Fetching Reddit mentions...")
        social = get_reddit_mentions(config.GAME_NAME)
        if not social:
            logger.error("❌ Failed to retrieve Reddit data")
        else:
            logger.info(f"✅ Retrieved Reddit data: {len(social)} records")
        
        # Process data only if we have at least one data source
        if not steam and not social:
            logger.error("💥 No data available from either source. Aborting.")
            return
            
        logger.info("🔄 Merging datasets...")
        merged = merge_data(steam, social)
        
        # Output results
        if merged.empty:
            logger.error("⚠️ Merged dataset is empty. No results to output.")
        else:
            logger.info("💾 Saving results to CSV...")
            merged.to_csv(config.CSV_FILENAME, index=False)
            logger.info(f"📊 Results saved to {config.CSV_FILENAME}")
            print(merged.to_markdown(index=False))
            
            # Generate plot
            logger.info("📈 Generating visualization...")
            plot_results(merged, config.GAME_NAME)
            logger.info(f"🖼️ Plot saved to {config.PLOT_FILENAME}")
        
        logger.info("🏁 Process completed!")

    except Exception as e:
        logger.error(f"🔥 Unexpected error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()