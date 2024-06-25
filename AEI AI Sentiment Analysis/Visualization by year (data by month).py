# Data Visualization for News Articles Sentiment Analysis (by month data/by year calculation):

import os
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import re

directory = '/Users/LindaSong/Desktop/AI Sentiment Results'

data = {'Year':[],
        'Percentage Positive':[],
        'Percentage Negative':[],
        'Percentage Neutral':[]}
df_count = pd.DataFrame(data)

year = 2000
pos_count = 0
neg_count = 0
neu_count = 0
total_count = 0

# Sort filenames
sorted_filenames = sorted(os.listdir(directory))

# Process each file
for filename in sorted_filenames:
    if filename.endswith('.csv'):
        # constructing full path
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        
        # get the number of years
        match = re.search(r'(\d+)',filename)

        if match:
            current_year = float(match.group(1))

        if current_year == year:
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

            new_row = {'Year': year,
            'Percentage Positive': pos_share,
            'Percentage Negative': neg_share,
            'Percentage Neutral': neu_share}

            df_count = df_count._append(new_row, ignore_index = True)

            year = current_year
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

df_count = df_count.sort_values(by='Year')
plt.plot(df_count['Year'], df_count['Percentage Positive'])
plt.plot(df_count['Year'], df_count['Percentage Negative'])
plt.plot(df_count['Year'], df_count['Percentage Neutral'])

plt.xlabel('Year')
plt.ylabel('Percentage of Articles')
plt.title('Sentiment Analysis')
plt.legend(['Positive','Negative','Neutral'])

plt.savefig('/Users/LindaSong/Desktop/plot 2.png')