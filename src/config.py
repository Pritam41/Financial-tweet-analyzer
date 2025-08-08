# src/config.py
import datetime

# --- Scraping Configuration ---
# IMPORTANT: Add your Twitter/X username and password here
TWITTER_USERNAME = "pritamgarud369"
TWITTER_PASSWORD = "Pritam@1234"

HASHTAGS = ["#nifty50", "#sensex"]
SINCE_DATE = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
UNTIL_DATE = datetime.date.today().strftime("%Y-%m-%d")
TWEET_LIMIT_PER_HASHTAG = 500 # Target number of tweets per hashtag

# --- Data Storage Paths ---
RAW_DATA_PATH = "data/raw/raw_tweets.parquet"
PROCESSED_DATA_PATH = "data/processed/processed_tweets.parquet"

# --- Analysis Configuration ---
VECTORIZER_MAX_FEATURES = 1000