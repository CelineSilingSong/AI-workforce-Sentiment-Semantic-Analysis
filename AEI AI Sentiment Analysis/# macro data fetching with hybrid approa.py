# macro data fetching with hybrid approach
# by Siling Song

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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException 

# Function to scrape meta data using Selenium and BeautifulSoup
def scrape_news_article(url):
    # Path to the ChromeDriver executable
    chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

    # Configure Chrome options (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode

    # Initialize Chrome WebDriver using Service and Options
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    try:
        # Navigate to the news article page
        driver.get(url)

        # Wait for some time to ensure page is fully loaded (adjust as needed)
        time.sleep(5)  # Example: wait for 5 seconds (can be adjusted)

        # Get the page source after JavaScript execution
        page_source = driver.page_source

        # Use BeautifulSoup to parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract meta tags
        metadata = {}

        # Extracting main meta tags:
        main_tags = ['title', 'description']
        for main_tag in main_tags:
            tag = soup.find('meta', attrs={'property': main_tag})
            if tag:
                metadata[main_tag] = tag['content']
            else:
                metadata[main_tag] = 'N/A'

        # Extracting keywords
        tag = soup.find('meta', attrs={'name': 'keywords'})
        if tag:
            metadata['keywords'] = tag['content']
        else:
            metadata['keywords'] = 'N/A'

        # Extract Open Graph tags
        og_tags = ['og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']
        for og_tag in og_tags:
            tag = soup.find('meta', attrs={'property': og_tag})
            if tag:
                metadata[og_tag] = tag['content']
            else:
                metadata[og_tag] = 'N/A'

        # Extract Twitter Card tags
        twitter_tags = ['twitter:card', 'twitter:site', 'twitter:title', 'twitter:description']
        for twitter_tag in twitter_tags:
            tag = soup.find('meta', attrs={'name': twitter_tag})
            if tag:
                metadata[twitter_tag] = tag['content']
            else:
                metadata[twitter_tag] = 'N/A'

        # Extract Schema.org markup (example)
        for tag in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(tag.string)
                if '@context' in json_data and 'schema.org' in json_data['@context']:
                    metadata.update(json_data)
            except json.JSONDecodeError:
                continue

        # Extract additional custom tags
        article_tags = ['article:type', 'article:section', 'article:summary']
        for article_tag in article_tags:
            tag = soup.find('meta', attrs={'name': article_tag})
            if tag:
                metadata[article_tag] = tag['content']
            else:
                tag = soup.find('meta', attrs={'property': article_tag})
                if tag:
                    metadata[article_tag] = tag['content']
                else:
                    metadata[article_tag] = 'N/A'

        # Find all <p> tags
        #paragraphs = soup.find_all('p')
        #content = ''

        # Loop through each <p> tag and print its text content
        #for paragraph in paragraphs:
        #    print(paragraph)


        return metadata

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage:
url = "https://news.google.com/rss/articles/CBMiemh0dHBzOi8vd3d3LmZvcmJlcy5jb20vc2l0ZXMvbG91aXNjb2x1bWJ1cy8yMDIwLzAxLzA1L2FpLXNwZWNpYWxpc3QtaXMtdGhlLXRvcC1lbWVyZ2luZy1qb2ItaW4tMjAyMC1hY2NvcmRpbmctdG8tbGlua2VkaW4v0gEA?oc=5"
metadata = scrape_news_article(url)
print(metadata)

