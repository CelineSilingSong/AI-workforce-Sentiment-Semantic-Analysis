# Google News Scrapping by language by topic
# 2024.06.27
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException 


ssl_context = ssl.create_default_context(cafile=certifi.where())

class GoogleNewsFeedScraper:
    def __init__(self, query, start_date, end_date, language, region, ceid, topic):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.language = language
        self.region = region
        self.ceid = ceid
        self.topic = topic

    def scrape_google_news_feed(self):
        start_date = self.start_date
        end_date = self.end_date
        formatted_query = '('
        for i in range(len(self.query)):
            row = self.query[i]
            if i == len(self.query) -1:
                for j in range(len(row)):
                    elem = row[j].replace(" ", "+")
                    if j == len(row) -1:
                        formatted_query += f'"{elem}")'
                    else:
                        formatted_query += f'"{elem}"+OR+'

            else:
                for j in range(len(row)):
                    elem = row[j].replace(" ", "+")
                    if j == len(row) -1:
                        formatted_query += f'"{elem}")+AND+('
                    else:
                        formatted_query += f'"{elem}"+OR+' 

        # ("AI"+OR+"artificial+intelligence")+AND+("jobs"+OR+"employment"+OR+"workforce")
        response = requests.get(f'https://news.google.com/rss/search?q={formatted_query}+after:{start_date}+before:{end_date}&hl={self.language}&gl={self.region}&ceid={self.ceid}', verify=certifi.where())
        feed = feedparser.parse(response.content)
        print(feed)
        titles = []
        links = []
        pubdates = []
        source_urls = []
        source_names = []

        if feed.entries:
            for entry in feed.entries:
                # Title
                title = entry.title
                titles.append(title)
                # URL link
                link = entry.link
                links.append(link)
                # Date
                pubdate = entry.published
                date_str = str(pubdate)
                date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                pubdates.append(formatted_date)
                # Source name and URL
                if 'source' in entry:
                    source_name = entry.source.title if 'title' in entry.source else None
                    source_url = entry.source.get('href') if 'href' in entry.source else None
                else:
                    source_name = None
                    source_url = None
                source_names.append(source_name)
                source_urls.append(source_url)

        else:
            print("Nothing Found!")

        data = {'URL link': links, 'Title': titles, 'Date': pubdates, 'Source': source_names, 'Source Link': source_urls}
        return data
    
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
    def fetch_article_metadata(url):
        # Path to the ChromeDriver executable
        chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

        # Configure Chrome options (optional)
        # Chrome_options = Options()
        # Chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode

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

            # extract article body:
            article_body = soup.find('article') or soup.find('div', class_ = 'content')
            if article_body:
                text = article_body.get_text()
                metadata['article text'] = text
            else:
                metadata['article text'] = 'N/A'

            # Loop through each <p> tag and print its text content
            # Dor paragraph in paragraphs:
            # print(paragraph)

            print(metadata)
            return metadata

        finally:
            # Close the WebDriver
            driver.quit()

    def convert_data_to_csv(self,start_date):
        directory = '/Users/LindaSong/Desktop/test'
        d1 = self.scrape_google_news_feed()
        df = pd.DataFrame(d1)
        csv_name = f"{self.topic} {self.language} {start_date}.csv"
        csv_name_new = csv_name.replace(" ", "_")
        csv_path = os.path.join(directory,csv_name_new)
        df.to_csv(csv_path, index=False)
