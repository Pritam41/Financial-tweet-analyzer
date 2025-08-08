# src/main.py
import os
import pandas as pd

from .config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from .scraper import run_scraper
from .processor import process_data
from .analysis import generate_signals

def main():
    """Main pipeline to run the full data collection and analysis system."""
    
    # --- 1. Data Collection ---
    print("--- Starting Step 1: Data Collection ---")
    raw_df = run_scraper()
    
    if raw_df is not None and not raw_df.empty:
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        raw_df.to_parquet(RAW_DATA_PATH, index=False)
        print(f"Raw data saved to {RAW_DATA_PATH}")
    else:
        print("Data collection failed or returned no data. Exiting.")
        return

    # --- 2. Data Processing ---
    print("\n--- Starting Step 2: Data Processing ---")
    processed_df = process_data(raw_df)
    
    if processed_df is not None and not processed_df.empty:
        os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
        processed_df.to_parquet(PROCESSED_DATA_PATH, index=False)
        print(f"Processed data saved to {PROCESSED_DATA_PATH}")
    else:
        print("Data processing failed or resulted in empty data. Exiting.")
        return

    # --- 3. Analysis & Signal Generation ---
    print("\n--- Starting Step 3: Analysis & Signal Generation ---")
    final_df = generate_signals(processed_df)

    if final_df is not None:
        print("\n--- Final Output ---")
        print("Sample of the final dataset with sentiment signals:")
        print(final_df[['hashtag_source', 'cleaned_content', 'sentiment_signal']].head())
        print(f"\nSuccessfully generated final dataset with {len(final_df)} entries.")

if __name__ == "__main__":
    main()