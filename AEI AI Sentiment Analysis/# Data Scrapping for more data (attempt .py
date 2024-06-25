# Data Scrapping for more data (attempt by month):
# June 10, 2024
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


ssl_context = ssl.create_default_context(cafile=certifi.where())

class GoogleNewsFeedScraper:
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
    
    def fetch_article_metadata(self,url):
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch the page at {url}")
            return {}

        soup = BeautifulSoup(response.content, 'html.parser')
        metadata = {}

        # Extracting main meta tags:
        main_tags = ['title','description']
        for main_tag in main_tags:
            tags = soup.find_all('meta', attrs = {'property': main_tag})
            if tags:
                tag = tags[0]
                metadata[main_tag] = tag['content']

        # Extracting keywords
        tags = soup.find_all('meta', attrs={'name': 'keywords'})
        if tags:
            tag = tags[0]
            if 'content' in tag.attrs:
                metadata['keywords'] = tag['content']
            else:
                metadata['keywords'] = 'N/A'

        # Extract Open Graph tags
        og_tags = ['og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']
        for og_tag in og_tags:
            tags = soup.find_all('meta',attrs = {'property':og_tag})
            if tags:
                tag = tags[0]
                if 'content' in tag.attrs:                    
                    metadata[og_tag] = tag['content']
                else:
                    metadata[og_tag] = 'N/A'

        # Extract Twitter Card tags
        twitter_tags = ['twitter:card', 'twitter:site', 'twitter:title', 'twitter:description']
        for twitter_tag in twitter_tags:
            tags = soup.find_all('meta',attrs={'name':twitter_tag})
            if tags:
                tag = tags[0]
                if 'content' in tag.attrs:                    
                    metadata[twitter_tag] = tag['content']
                else:
                    metadata[twitter_tag] = 'N/A'

        # Extract Schema.org markup
        for tag in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(tag.string)
                if '@context' in json_data and 'schema.org' in json_data['@context']:
                    metadata.update(json_data)
            except json.JSONDecodeError:
                continue

        # Extract article type & sections
        article_tags = ['article.type', 'article.section', 'article.summary']
        for article_tag in article_tags:
            tags = soup.find_all('meta', attrs={'name':article_tag})
            if tags:
                tag=tags[0]
                if 'content' in tag.attrs:                    
                    metadata[article_tag] = tag['content']
                else:
                    metadata[article_tag] = 'N/A'
            
        return metadata

    def scrape_google_news_feed(self):
        start_date = self.start_date
        end_date = self.end_date
        #rss_url = f'https://news.google.com/rss/search?q={formatted_query}+after:{start_date}+before:{end_date}&hl=en-IN&gl=IN&ceid=IN:en'
        #feed = feedparser.parse(rss_url)
        response = requests.get(f'https://news.google.com/rss/search?q=("AI"+OR+"artificial+intelligence")+AND+("jobs"+OR+"employment"+OR+"workforce")+after:{start_date}+before:{end_date}&hl=en-IN&gl=IN&ceid=IN:en', verify=certifi.where())
        feed = feedparser.parse(response.content)
        print(feed)
        titles = []
        links = []
        pubdates = []

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


        else:
            print("Nothing Found!")

        data = {'URL link': links, 'Title': titles, 'Date': pubdates}
        return data

    def convert_data_to_csv(self,int):
        directory = '/Users/LindaSong/Desktop/AI job 4'
        d1 = self.scrape_google_news_feed()
        df = pd.DataFrame(d1)
        csv_name = self.query + f"{int}.csv"
        csv_name_new = csv_name.replace(" ", "_")
        csv_path = os.path.join(directory,csv_name_new)
        df.to_csv(csv_path, index=False)

# Define number of periods per month
periods_per_month = 6

# Initialize lists to store start and end dates
start_dates = []
end_dates = []

# Function to calculate date ranges for each period in a month
def split_month_into_periods(year, month, periods):
    first_day_of_month = datetime(year, month, 1)
    if month == 12:
        last_day_of_month = datetime(year, month, 31)
    else:
        last_day_of_month = datetime(year, month % 12 + 1, 1) - timedelta(days=1)
    
    days_in_month = (last_day_of_month - first_day_of_month).days + 1
    period_length = days_in_month // periods
    extra_days = days_in_month % periods

    current_start_date = first_day_of_month
    for i in range(periods):
        current_end_date = current_start_date + timedelta(days=period_length - 1)
        if i < extra_days:
            current_end_date += timedelta(days=1)
        start_dates.append(current_start_date.strftime('%Y-%m-%d'))
        end_dates.append(current_end_date.strftime('%Y-%m-%d'))
        current_start_date = current_end_date + timedelta(days=1)

# Loop through the years and months to generate date ranges
for year in np.arange(2020, 2025):
    for month in np.arange(1, 13):
        split_month_into_periods(year, month, periods_per_month)

# Create a DataFrame to display the date ranges
df_time = pd.DataFrame({'Start Dates': start_dates, 'End Dates': end_dates})
print(df_time)

query = 'AI Job'
for index, row in df_time.iterrows():
    start_date = row[0]
    end_date = row[1]
    scraper = GoogleNewsFeedScraper(query, start_date, end_date)
    scraper.convert_data_to_csv(start_date)
    print("success")