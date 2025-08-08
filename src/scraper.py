# src/scraper.py (Final Corrected Version)
import time
import logging
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import (
    TWITTER_USERNAME, TWITTER_PASSWORD, HASHTAGS,
    TWEET_LIMIT_PER_HASHTAG
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # You can now add "--headless" to run the browser in the background
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("log-level=3")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logging.error(f"Failed to setup WebDriver: {e}")
        return None

def login(driver):
    if TWITTER_USERNAME == "YOUR_USERNAME_HERE" or TWITTER_PASSWORD == "YOUR_PASSWORD_HERE":
        logging.error("Username and Password are not set in src/config.py.")
        return False
    try:
        logging.info("Navigating to login page...")
        driver.get("https://twitter.com/login")
        wait = WebDriverWait(driver, 20)

        username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(TWITTER_USERNAME)
        driver.find_element(By.XPATH, '//span[contains(text(),"Next")]').click()

        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(TWITTER_PASSWORD)
        driver.find_element(By.XPATH, '//span[contains(text(),"Log in")]').click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')))
        logging.info("Login successful! Home page is ready.")
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        driver.save_screenshot('login_error.png')
        return False

def search_and_scrape_hashtag(driver, hashtag):
    tweets_collected = []
    logging.info(f"Starting search for {hashtag}...")
    try:
        wait = WebDriverWait(driver, 15)
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')))
        search_input.clear()
        search_input.send_keys(hashtag)
        search_input.send_keys(Keys.ENTER)

        latest_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Latest")]')))
        latest_tab.click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]')))
        logging.info(f"On 'Latest' tab for {hashtag}. Starting scroll...")

        last_height = driver.execute_script("return document.body.scrollHeight")
        unique_tweets = set()
        while len(unique_tweets) < TWEET_LIMIT_PER_HASHTAG:
            articles = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            for article in articles[-10:]:
                try:
                    tweet_text = article.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                    if tweet_text not in unique_tweets:
                        unique_tweets.add(tweet_text)
                except Exception:
                    continue
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info(f"Reached end of page for {hashtag}.")
                break
            last_height = new_height
        tweets_collected = list(unique_tweets)
        logging.info(f"Scraped {len(tweets_collected)} unique tweets for {hashtag}.")
    except Exception as e:
        logging.error(f"Failed during search/scrape for {hashtag}: {e}")
        driver.save_screenshot(f"error_scraping_{hashtag}.png")
    return tweets_collected

def run_scraper():
    driver = setup_driver()
    if not driver:
        return None
    all_tweets_data = []
    try:
        if login(driver):
            for i, hashtag in enumerate(HASHTAGS):
                tweets = search_and_scrape_hashtag(driver, hashtag)
                for tweet in tweets:
                    all_tweets_data.append({'hashtag_source': hashtag, 'content': tweet})

                # *** THE FIX IS HERE ***
                # After finishing a hashtag, go back to the home page to ensure a clean state for the next search.
                if i < len(HASHTAGS) - 1:
                    logging.info("Returning to home page to reset for next search.")
                    driver.get("https://twitter.com/home")
                    # Also, add a random wait to be less bot-like
                    time.sleep(random.uniform(5, 10))
    finally:
        logging.info("Scraping finished. Closing driver.")
        driver.quit()
    if not all_tweets_data:
        return None
    return pd.DataFrame(all_tweets_data)