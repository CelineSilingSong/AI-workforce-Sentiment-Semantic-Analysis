# Data Visualization For News Articles by month post 2020
# by Siling Song

import os
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import re
from datetime import datetime

directory = '/Users/LindaSong/Desktop/AI Sentiment Results 3'

data = {'Month':[],
        'Percentage Positive':[],
        'Percentage Negative':[],
        'Percentage Neutral':[]}
df_count = pd.DataFrame(data)

year = 2020
month = 1
pos_count = 0
neg_count = 0
neu_count = 0
total_count = 0

# Sort filenames
sorted_filenames = sorted(os.listdir(directory))
print(sorted_filenames)

# Process each file
for filename in sorted_filenames:
    if filename.endswith('.csv'):
        # constructing full path
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        
        # Define a regex pattern to match the month '01'
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})',filename)

        if match:
            current_year = int(match.group(1))
            print(f'current year is {current_year}')
            current_month = int(match.group(2))
            print(f'current month is {current_month}')
        if (current_year == year) & (current_month == month):
            for index, row in df.iterrows():
                if row[6] == 'Positive':
                    pos_count +=1
                    total_count +=1
                elif row[6] == 'Negative':
                    neg_count += 1
                    total_count += 1
                else:
                    neu_count += 1
                    total_count += 1
        
        else:
            pos_share = pos_count/total_count
            neg_share = neg_count/total_count
            neu_share = neu_count/total_count
            date = datetime(year,month,1)
            new_row = {'Month': date,
            'Percentage Positive': pos_share,
            'Percentage Negative': neg_share,
            'Percentage Neutral': neu_share}

            df_count = df_count._append(new_row, ignore_index = True)

            year = current_year
            month = current_month
            pos_count = 0
            neg_count = 0
            neu_count = 0
            total_count = 0

            for index, row in df.iterrows():
                if row[6] == 'Positive':
                    pos_count +=1
                    total_count +=1
                elif row[6] == 'Negative':
                    neg_count += 1
                    total_count += 1
                else:
                    neu_count += 1
                    total_count += 1

df_count = df_count.sort_values(by='Month')
plt.plot(df_count['Month'], df_count['Percentage Positive'])
plt.plot(df_count['Month'], df_count['Percentage Negative'])
plt.plot(df_count['Month'], df_count['Percentage Neutral'])

plt.xlabel('Month')
plt.ylabel('Percentage of Articles')
plt.title('Sentiment Analysis')
plt.legend(['Positive','Negative','Neutral'])

plt.xticks(rotation = 'vertical')

plt.tight_layout()
plt.savefig('/Users/LindaSong/Desktop/plot 3.png')