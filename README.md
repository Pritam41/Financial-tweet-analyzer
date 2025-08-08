# Real-Time Market Intelligence System

A Python-based data pipeline that scrapes, processes, and analyzes financial discussions from Twitter/X to generate quantitative market sentiment signals. This project demonstrates a complete data engineering workflow, from robust data collection to insightful analysis.

---

## 🚀 Features

- **Robust Web Scraping:** Uses Selenium to automate a browser, handle logins, and navigate dynamic web pages, making it resilient to anti-scraping measures.
- **Intelligent Rate Limiting:** Mimics human behavior with randomized delays to avoid `429 (Too Many Requests)` errors.
- **Efficient Data Processing:** Cleans and normalizes raw text data using regular expressions and stores it in the efficient Parquet format.
- **Quantitative Signal Generation:** Implements TF-IDF to convert unstructured tweet data into a numerical sentiment/momentum signal, ready for analysis.
- **Modular & Maintainable Code:** Well-structured project with separate modules for configuration, scraping, processing, and analysis.

---

## 🛠️ Setup and Installation

Follow these steps to set up and run the project.

### Prerequisites

- Python 3.8+
- Google Chrome browser installed

### 1. Clone the Repository

```bash
git clone ([https://github.com/Pritam41/Financial-tweet-analyzer.git])
cd Financial-tweet-analyzer
```

### 2. Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment (on Windows)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install pandas selenium webdriver-manager pyarrow scikit-learn
```

### 4. Configure Credentials

Open the `src/config.py` file and enter your Twitter/X login credentials:

```python
# src/config.py
TWITTER_USERNAME = "your_twitter_username"
TWITTER_PASSWORD = "your_twitter_password"
```

---

## ▶️ How to Run

With the virtual environment activated, run the main script from the project's root directory:

```bash
python -m src.main
```

The script will launch a Chrome browser and execute the entire pipeline. Final data files will be saved in the `data/` directory.
