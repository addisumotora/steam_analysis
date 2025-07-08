# Steam Game Analytics Tracker

This solution tracks follower dynamics on Steam and social media mentions, providing daily analytics and visualizations.

## Features
- Steam follower history extraction from SteamDB
- Reddit mention tracking using PRAW API
- Daily data aggregation
- CSV export and visualization
- Configurable game parameters

## How It Works

1. **Steam Data Collection**: Fetches follower history for the configured Steam game (by AppID) from SteamDB. If SteamDB blocks the request, Steam data will be empty.
2. **Reddit Mentions Collection**: Uses the Reddit API (PRAW) to search for mentions of the game name across all subreddits for the last 30 days. Only public Reddit data is used (no login required).
3. **Data Merging**: Steam and Reddit data are merged by date. If one source is missing for a date, it is filled with zero.
4. **Output**:
   - The merged data is saved as a CSV file in `data/results.csv`.
   - A visualization (plot) comparing Steam followers and Reddit mentions is saved as `data/results.png`.
   - The merged data is also printed in markdown table format in the terminal.

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root with your Reddit API credentials:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_app_name
```

### 3. Run the tracker

```bash
python src/main.py
```

### 4. Output

- Results CSV: `data/results.csv`
- Plot image: `data/results.png`