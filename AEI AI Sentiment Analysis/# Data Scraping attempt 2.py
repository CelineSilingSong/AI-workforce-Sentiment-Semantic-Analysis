# Data Scraping attempt 2

import feedparser
import pandas as pd
from datetime import datetime
import ssl
import certifi
import requests
import numpy as np


ssl_context = ssl.create_default_context(cafile=certifi.where())

class GoogleNewsFeedScraper:
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date

    def scrape_google_news_feed(self):
        formatted_query = '%20'.join(self.query.split())
        start_date = self.start_date
        end_date = self.end_date
        #rss_url = f'https://news.google.com/rss/search?q={formatted_query}+after:{start_date}+before:{end_date}&hl=en-IN&gl=IN&ceid=IN:en'
        #feed = feedparser.parse(rss_url)
        response = requests.get(f'https://news.google.com/rss/search?q={formatted_query}+after:{start_date}+before:{end_date}&hl=en-IN&gl=IN&ceid=IN:en', verify=certifi.where())
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
        d1 = self.scrape_google_news_feed()
        df = pd.DataFrame(d1)
        csv_name = self.query + f"{int}.csv"
        csv_name_new = csv_name.replace(" ", "_")
        df.to_csv(csv_name_new, index=False)


for year in np.arange(2000,2025):
    query = 'AI Job'
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    scraper = GoogleNewsFeedScraper(query, start_date, end_date)
    scraper.convert_data_to_csv(year)
    print("success")