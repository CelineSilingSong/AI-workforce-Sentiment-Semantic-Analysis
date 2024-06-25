# Fetching Macro Level Data
# June 20, 2024
# By Siling Song

import feedparser
import pandas as pd
from datetime import datetime, timedelta
import ssl
import certifi
import requests
import numpy as np
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random

# specify the ssl certificate context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# speficy the path to the ChromeDriver executable
chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Example of adding a headless argument
# Initialize Chrome WebDriver using Service and Options
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Path to directory:
directory_path = '/Users/LindaSong/Desktop/AI job 3'

def fetch_article_metadata(url):
    # initialize metadata dictionary:
    metadata = {}
    # tags to extract:
    name_tags = ['keywords', 'twitter:card', 'twitter:site', 'twitter:title', 'twitter:description','article.type', 'article.section', 'article.summary']
    property_tags = ['title','description','og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']

    try:
        driver.get(url)

        # Wait for specific element to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'specific-element-css-selector'))
        )

        for name_tag in name_tags:
            tag = driver.find_element_by_css_selector(f'meta[name="{name_tag}"]')
            if tag:
                metadata[name_tag] = tag.get_attribute('content')
            else:
                metadata[name_tag] = 'N/A'

        for property_tag in property_tags:
            tag = driver.find_element_by_css_selector(f'meta[property="{property_tag}]')
            if tag:
                metadata[property_tag] = tag.get_attribute('content')
            else:
                metadata[name_tag] = 'N/A'
        return metadata

    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
        
            

def main():



    files = os.listdir(directory_path)

    for file in files:
        file_path = os.path.join(directory_path,file)
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            url = row[0]

            # Scrape with random delay
            delay = random.uniform(1, 3)  # Random delay between 1 to 3 seconds
            time.sleep(delay)

            meta_data = fetch_article_metadata(url)
            if meta_data:
                print(f"obtained metadata successfully")
                meta_data_df = pd.DataFrame(meta_data)
                df = pd.concat([df,meta_data_df], axis = 1)
            else:
                print(f"Failed to scrape {url}")

        df.to_csv(f'/Users/LindaSong/Desktop/AI job 5/meta {file}')
    driver.quit()

if __name__ == "__main__":
    main()



