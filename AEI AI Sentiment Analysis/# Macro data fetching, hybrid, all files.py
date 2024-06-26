# Macro data fetching, hybrid, all files
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


# Function to flatten JSON data
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Function to scrape meta data using Selenium and BeautifulSoup
def scrape_news_article(url):
    # Path to the ChromeDriver executable
    chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

    # Configure Chrome options (optional)
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode

    # Initialize Chrome WebDriver using Service and Options
    driver = webdriver.Chrome(service=Service(chrome_driver_path))

    try:
        # Navigate to the news article page
        driver.get(url)

        # Wait for some time to ensure page is fully loaded
        time.sleep(8)  

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
            if not tag:
                tag = soup.find('meta', attrs={'name': main_tag})
            if tag and 'content' in tag.attrs:
                metadata[main_tag] = tag['content']
            else:
                metadata[main_tag] = 'N/A'

        # Extracting keywords
        tag = soup.find('meta', attrs={'name': 'keywords'})
        if tag and 'content' in tag.attrs:
            metadata['keywords'] = tag['content']
        else:
            metadata['keywords'] = 'N/A'

        # Extract Open Graph tags
        og_tags = ['og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']
        for og_tag in og_tags:
            tag = soup.find('meta', attrs={'property': og_tag})
            if not tag:
                tag = soup.find('meta', attrs={'name': og_tag})
            if tag and 'content' in tag.attrs:
                metadata[og_tag] = tag['content']
            else:
                metadata[og_tag] = 'N/A'

        # Extract Twitter Card tags
        twitter_tags = ['twitter:card', 'twitter:site', 'twitter:title', 'twitter:description']
        for twitter_tag in twitter_tags:
            tag = soup.find('meta', attrs={'name': twitter_tag})
            if not tag:
                tag = soup.find('meta', attrs={'property': twitter_tag})
            if tag and 'content' in tag.attrs:
                metadata[twitter_tag] = tag['content']
            else:
                metadata[twitter_tag] = 'N/A'

        # Extract Schema.org markup (example)
        schema_data = []
        for tag in soup.find_all('script', type='application/ld+json'):
            if tag.string:
                try:
                    json_data = json.loads(tag.string)
                    if '@context' in json_data and 'schema.org' in json_data['@context']:
                        flattened_data = flatten_json(json_data)
                        schema_data.append(flattened_data)
                        metadata.update(json_data)
                except json.JSONDecodeError:
                    continue
            
        # Extract additional custom tags
        article_tags = ['article:type', 'article:section', 'article:summary']
        for article_tag in article_tags:
            tag = soup.find('meta', attrs={'name': article_tag})
            if not tag:
                tag = soup.find('meta', attrs={'property': article_tag})
            if tag and 'content' in tag.attrs:
                metadata[article_tag] = tag['content']
            else:
                metadata[article_tag] = 'N/A'

        # Find all <p> tags
        #paragraphs = soup.find_all('p')
        #content = ''

        # Loop through each <p> tag and print its text content
        # Dor paragraph in paragraphs:
        # print(paragraph)

        print(metadata)
        return metadata

    finally:
        # Close the WebDriver
        driver.quit()

## Example usage:
#
## Path to the ChromeDriver executable
#chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'
## Configure Chrome options (optional)
#chrome_options = Options()
#chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode
## Initialize Chrome WebDriver using Service and Options
#driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
#url = "https://news.google.com/rss/articles/CBMiemh0dHBzOi8vd3d3LmZvcmJlcy5jb20vc2l0ZXMvbG91aXNjb2x1bWJ1cy8yMDIwLzAxLzA1L2FpLXNwZWNpYWxpc3QtaXMtdGhlLXRvcC1lbWVyZ2luZy1qb2ItaW4tMjAyMC1hY2NvcmRpbmctdG8tbGlua2VkaW4v0gEA?oc=5"
#metadata = scrape_news_article(url,driver)
#print(metadata)

# Path to directory:
directory_path = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/AEI AI Sentiment Analysis/AI Job To Fetch Meta 2020 Jan'

def main():
    
    files = os.listdir(directory_path)

    for file in files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)
        
        all_metadata = []

        for index, row in df.iterrows():
            url = row[0]

            meta_data = scrape_news_article(url)
            if meta_data:
                print(f"Obtained metadata successfully for {url}")
                all_metadata.append(meta_data)
            else:
                print(f"Failed to scrape {url}")

        if all_metadata:
            meta_data_df = pd.DataFrame(all_metadata)
            df = pd.concat([df, meta_data_df], axis=1)
            df.to_csv(f'/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/AEI AI Sentiment Analysis/AI Job Meta Data Fetched 2020 Jan/meta_{file}', index=False)
        else:
            print(f"No metadata collected for {file}")


if __name__ == "__main__":
    main()


