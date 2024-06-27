import numpy as np
from datetime import datetime, timedelta
from 


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

query = np.array([
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'LLM', 'Generative AI', 'Machine Learning', 'Neural Network', 'Deep Learning'],
    ['Job', 'Work', 'Workforce', 'Occupation', 'Career', 'Labor Market', 'Labor'],
])

for index, row in df_time.iterrows():
    start_date = row[0]
    end_date = row[1]
    scraper = GoogleNewsFeedScraper(query, start_date, end_date)
    scraper.convert_data_to_csv(start_date)
    print("success")

query = np.array([
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'LLM', 'Generative AI', 'Machine Learning', 'Neural Network', 'Deep Learning'],
    ['Job', 'Work', 'Workforce', 'Occupation', 'Career', 'Labor Market', 'Labor', 'employment']
])

query = np.array([
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'LLM', 'Generative AI'],
    ['Job', 'Work', 'Workforce', 'Occupation', 'Career']
])
# https://news.google.com/rss/search?q=(%22AI%22+OR+%22Artificial+Intelligence%22+OR+%22Large+Language+Models%22+OR+%22Machine+Learning%22)+AND+(%22Job%22+OR+%22Work%22+OR+%22Workforce%22+OR+%22Occupation%22+OR+%22Career%22)+after:2018-02-01+before:2018-02-08&hl=en-IN&gl=IN&ceid=IN:en
query = np.array([
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'Generative AI','Machine Learning'],
    ['Job', 'Work', 'Workforce', 'Career', 'employment']
])

query = [
    ['Tech'],
    ['AI', 'Artificial Intelligence', 'Large Language Models', 'Generative AI'],
    ['Job', 'Work', 'Workforce', 'employment']
]

formatted_query = '('
for i in range(len(query)):
    row = query[i]
    if i == len(query) -1:
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
print(formatted_query)

string = f'https://news.google.com/rss/search?q={formatted_query}+after:2018-01-01+before:2018-01-08&hl=en-US&gl=US&ceid=US:en'

print(string)