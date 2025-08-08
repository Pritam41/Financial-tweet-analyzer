# src/analysis.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

from .config import VECTORIZER_MAX_FEATURES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_signals(df: pd.DataFrame):
    """Converts textual data into quantitative signals using TF-IDF."""
    if df is None or df.empty or 'cleaned_content' not in df.columns:
        logging.warning("Input DataFrame for analysis is invalid. Skipping signal generation.")
        return None

    logging.info("Generating quantitative signals using TF-IDF...")
    
    vectorizer = TfidfVectorizer(
        max_features=VECTORIZER_MAX_FEATURES,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(df['cleaned_content'])
        
        # Create a composite signal by summing TF-IDF scores.
        # This is a basic form of sentiment/momentum scoring.
        df['sentiment_signal'] = tfidf_matrix.sum(axis=1)
        
        logging.info("Successfully generated TF-IDF signals.")
        print("\n--- Top Keywords Driving Signals ---")
        feature_names = vectorizer.get_feature_names_out()
        print(f"Sample of top keywords: {feature_names[:20]}")
        
        return df
    except Exception as e:
        logging.error(f"Error during TF-IDF vectorization: {e}")
        return None