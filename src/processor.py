# src/processor.py
import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_tweet_content(text):
    """Cleans tweet text by removing URLs, mentions, hashtags, and non-alphanumeric characters."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    text = text.lower().strip()
    return text

def process_data(df: pd.DataFrame):
    """Applies all processing steps to the raw dataframe."""
    if df is None or df.empty:
        logging.warning("Input DataFrame is empty. Skipping processing.")
        return None

    logging.info("Starting data processing and cleaning...")
    
    # 1. Deduplication
    initial_rows = len(df)
    df.drop_duplicates(subset=['content'], inplace=True)
    logging.info(f"Removed {initial_rows - len(df)} duplicate tweets.")
    
    # 2. Clean tweet content
    df['cleaned_content'] = df['content'].apply(clean_tweet_content)
    
    # 3. Remove rows where cleaned content is empty
    df = df[df['cleaned_content'] != ''].copy()
    
    logging.info(f"Processing complete. {len(df)} tweets remaining.")
    return df