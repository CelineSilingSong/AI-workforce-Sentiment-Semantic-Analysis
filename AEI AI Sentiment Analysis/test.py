import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from DataScraper import GoogleNewsFeedScraper
from googletrans import Translator


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
for year in np.arange(2018, 2025):
    for month in np.arange(1, 13):
        split_month_into_periods(year, month, periods_per_month)

# Create a DataFrame to display the date ranges
df_time = pd.DataFrame({'Start Dates': start_dates, 'End Dates': end_dates})
print(df_time)

# Full list of keywords
# query = np.array([
#     ['AI', 'Artificial Intelligence', 'Large Language Models', 'LLM', 'Generative AI', 'Machine Learning', 'Neural Network', 'Deep Learning'],
#     ['Job', 'Work', 'Workforce', 'Occupation', 'Career', 'Labor Market', 'Labor'],
# ])

# https://news.google.com/rss/search?q=(%22AI%22+OR+%22Artificial+Intelligence%22+OR+%22Large+Language+Models%22+OR+%22Machine+Learning%22)+AND+(%22Job%22+OR+%22Work%22+OR+%22Workforce%22+OR+%22Occupation%22+OR+%22Career%22)+after:2018-02-01+before:2018-02-08&hl=en-IN&gl=IN&ceid=IN:en

# Language Codes:
# English (US): hl=en-US
# English (UK): hl=en-GB
# Spanish (Spain): hl=es-ES
# Spanish (Latin America): hl=es-419
# French (France): hl=fr-FR
# German (Germany): hl=de-DE
# Italian (Italy): hl=it-IT
# Portuguese (Brazil): hl=pt-BR
# Portuguese (Portugal): hl=pt-PT
# Chinese (Simplified): hl=zh-CN
# Chinese (Traditional): hl=zh-TW
# Japanese (Japan): hl=ja-JP
# Korean (Korea): hl=ko-KR
# Russian (Russia): hl=ru-RU
# Arabic (Middle East): hl=ar
# Hindi (India): hl=hi-IN

# Region Codes:
# United States: gl=US
# United Kingdom: gl=GB
# Spain: gl=ES
# France: gl=FR
# Germany: gl=DE
# Italy: gl=IT
# Brazil: gl=BR
# Portugal: gl=PT
# China: gl=CN
# Taiwan: gl=TW
# Japan: gl=JP
# Korea: gl=KR
# Russia: gl=RU
# India: gl=IN
# Mexico: gl=MX
# Canada: gl=CA
# Australia: gl=AU

# to be fixed
locale = {
    'languages':['en-US', 'en-GB','es-ES','es-419','fr-FR','de-DE','it-IT','pt-BR','pt-PT','zh-CN','gl=TW','gl=JP','gl=KR', 'gl=RU', 'gl=IN', 'gl=MX', 'gl=CA','gl=AU'],
    'regions':[],
    'ceids':[]
}
languages = 'en-US'
regions = 'US'
ceids = 'US:en'
topics = 'xx'

query = [
    [topic],
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'Generative AI'],
    ['Job', 'Work', 'Workforce', 'employment']
]

for index, row in df_time.iterrows():
    start_date = row[0]
    end_date = row[1]
    scraper = GoogleNewsFeedScraper(query, start_date, end_date, language, region, ceid, topic)
    scraper.convert_data_to_csv(start_date)
    print("success")