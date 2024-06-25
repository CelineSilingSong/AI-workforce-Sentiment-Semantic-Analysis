import requests
import pandas as pd
from textblob import TextBlob
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Define a function to fetch articles from Google News with retry mechanism
def fetch_google_news_articles_with_retry(keyword):
    url = f'https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en'
    session = requests.Session()
    retry_strategy = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504], backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch articles: {e}")
        return None

# Define a function to extract article information
def extract_article_info(feed):
    articles = []
    # Use BeautifulSoup to parse the RSS feed
    soup = BeautifulSoup(feed, 'xml')
    entries = soup.find_all('item')
    
    for entry in entries:
        title = entry.title.text
        link = entry.link.text
        published = entry.pubDate.text
        article = {'title': title, 'link': link, 'published': published}
        articles.append(article)
        
    return articles

# Define a function to filter articles by date
def filter_articles_by_date(articles, from_date, to_date):
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    filtered_articles = []

    for article in articles:
        published_date = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %Z')
        if from_date <= published_date <= to_date:
            filtered_articles.append(article)

    return filtered_articles

# Define a function to get article titles and information for a date range
def get_articles_info(keyword, from_date, to_date):
    all_articles = []
    current_date = datetime.strptime(from_date, '%Y-%m-%d')
    end_date = datetime.strptime(to_date, '%Y-%m-%d')

    while current_date <= end_date:
        next_date = current_date + timedelta(days=30)
        if next_date > end_date:
            next_date = end_date

        feed = fetch_google_news_articles_with_retry(keyword)
        if feed:
            articles = extract_article_info(feed)
            filtered_articles = filter_articles_by_date(articles, current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            all_articles.extend(filtered_articles)
        
        current_date = next_date + timedelta(days=1)
    
    return all_articles

# Define a function to calculate sentiment
def calculate_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Define the main function to fetch articles, calculate sentiment, and save to CSV
def main():
    keyword = 'AI'
    from_date = '2010-01-01'
    to_date = '2024-05-26'
    
    articles = get_articles_info(keyword, from_date, to_date)
    if articles:
        print(f"Number of articles fetched: {len(articles)}")
        df = pd.DataFrame(articles)
        df['sentiment'] = df['title'].apply(calculate_sentiment)
        df['Sentiment Class'] = np.where(df['sentiment'] < 0, "negative",
                                          np.where(df['sentiment'] > 0, "positive", "neutral"))
        df.to_csv('/Users/LindaSong/Desktop/AI_sentiment_analysis.csv', index=False)
        print("CSV file saved successfully.")
    else:
        print("No articles fetched. CSV file not saved.")

# Call the main function
main()