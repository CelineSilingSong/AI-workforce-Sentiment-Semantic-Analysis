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

# translator
translator = Translator()

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


# to be fixed
languages_info = [
    {'dest':'en','hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'},
    {'dest':'en','hl': 'en-GB', 'gl': 'GB', 'ceid': 'GB:en'},
    {'dest':'es','hl': 'es-ES', 'gl': 'ES', 'ceid': 'ES:es'},
    {'dest':'es','hl': 'es-419', 'gl': 'MX', 'ceid': 'MX:es-419'},
    {'dest':'fr','hl': 'fr-FR', 'gl': 'FR', 'ceid': 'FR:fr'},
    {'dest':'de','hl': 'de-DE', 'gl': 'DE', 'ceid': 'DE:de'},
    {'dest':'it','hl': 'it-IT', 'gl': 'IT', 'ceid': 'IT:it'},
    {'dest':'pt','hl': 'pt-BR', 'gl': 'BR', 'ceid': 'BR:pt-BR'},
    {'dest':'pt','hl': 'pt-PT', 'gl': 'PT', 'ceid': 'PT:pt'},
    {'dest':'zh-cn','hl': 'zh-CN', 'gl': 'CN', 'ceid': 'CN:zh-CN'},
    {'dest':'zh-tw','hl': 'zh-TW', 'gl': 'TW', 'ceid': 'TW:zh-TW'},
    {'dest':'ja','hl': 'ja-JP', 'gl': 'JP', 'ceid': 'JP:ja-JP'},
    {'dest':'ko','hl': 'ko-KR', 'gl': 'KR', 'ceid': 'KR:ko-KR'},
    {'dest':'ru','hl': 'ru-RU', 'gl': 'RU', 'ceid': 'RU:ru-RU'},
    {'dest':'hi','hl': 'hi-IN', 'gl': 'IN', 'ceid': 'IN:hi-IN'},
    {'dest':'en','hl': 'en-IN', 'gl': 'IN', 'ceid': 'IN:en-IN'},
    {'dest':'en','hl': 'en-CA', 'gl': 'CA', 'ceid': 'CA:en'},
    {'dest':'en','hl': 'en-AU', 'gl': 'AU', 'ceid': 'AU:en'},
    {'dest':'fr','hl': 'fr-CA', 'gl': 'CA', 'ceid': 'CA:fr'},
    {'dest':'ar','hl': 'ar', 'gl': 'SA', 'ceid': 'SA:ar'}
]

topics = ['Education', 'Tech', 'Business', 'Politics', 'Regulation']

query = [
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'Generative AI'],
    ['Job', 'Work', 'Workforce', 'employment']
]

def translate_query(query, language):
    # Translate each element in the nested array

    translated_double_array = []
    for inner_array in query:
        translated_inner_array = []
        for text in inner_array:
            try:
                translated = translator.translate(text, dest=language)  # Translate to French as an example
            except Exception as e:
                print(f"Error occured when translating {text} into {language}:{e} ")
            translated_inner_array.append(translated.text)
        translated_double_array.append(translated_inner_array)
        print (translated_double_array)
    return translated_double_array


for index, row in df_time.iterrows():
    start_date = row[0]
    end_date = row[1]
    for topic in topics:
        for language_info in languages_info:
            translated_topic = translator.translate(topic, language_info['dest']).text
            translated_query = translate_query(query,language_info['dest'])
            scraper = GoogleNewsFeedScraper(translated_query, start_date, end_date, language_info['hl'], language_info['gl'], language_info['ceid'], translated_topic)
            scraper.convert_data_to_csv(start_date)
            print("success")