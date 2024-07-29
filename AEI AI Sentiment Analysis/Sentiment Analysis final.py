

import os
import pandas as pd
from LanguageAnalyzer import SentimentAnalyser
import re
from datetime import datetime
import matplotlib.pyplot as plt

# conducting sentiment analysis
# sentiment_analyser = SentimentAnalyser()
# 
# directory = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/preprocessed-en'
# 
# for filename in os.listdir(directory):
#     if filename.endswith('.csv'):
#         # constructing full path
#         file_path = os.path.join(directory, filename)
#         df = pd.read_csv(file_path)
#         # conducting sentiment analysis
#         df['Value']= df['Preprocessed Text'].astype(str).apply(sentiment_analyser.Return_Score_nltk)
#         df['Sentiment'] = df['Value'].apply(sentiment_analyser.Return_Sentiment_nltk)
#         # df.to_csv(f'/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/sentiment-en/{filename}', index = False)
# 

# Conducting alternative sentiment analysis:
sentiment_analyzer = SentimentAnalyser()
directory = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/preprocessed-en'
method = sentiment_analyzer.Sentiment_analysis_spacy

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        print(filename)
        # constructing full path
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        # conducting sentiment analysis
        df[['Value', 'Sentiment']] = df['Preprocessed Text'].astype(str).apply(lambda text: pd.Series(method(text)))
        df.to_csv(f'/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/ex-sentiment-en/{filename}', index = False)

# returns standardized date-time. 
def extract_year_month(date_string):
    # Define the pattern to match the year and month
    pattern = r'(\d{4})-(\d{2})'
    
    # Search for the pattern in the string
    match = re.search(pattern, date_string)
    
    # If a match is found, extract the year and month
    if match:
        year = int(match.group(1))  # The first group (year)
        month = int(match.group(2))  # The second group (month)
        date = datetime(year,month,1)
        return date
    else:
        return None, None  # Return None if no match is found
    

analyzed_directory = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/ex-sentiment-en'

sorted_filenames =sorted([filename for filename in os.listdir(analyzed_directory) if filename.endswith('.csv')])


data = {'Year':[],
        'Percentage Positive':[],
        'Percentage Negative':[],
        'Percentage Neutral':[]}
df_count = pd.DataFrame(data)

# Process each file
for filename in sorted_filenames:
    if filename.endswith('.csv'):
        # constructing full path
        file_path = os.path.join(analyzed_directory, filename)
        df = pd.read_csv(file_path)

        date = extract_year_month(filename)
        
        pos_count = 0
        neg_count = 0
        neu_count = 0
        total_count = 0

        print(df.columns)
        
        for index, row in df.iterrows():
            
            if str(row['Sentiment']).lower().replace(' ','') == 'positive':
                pos_count +=1
                total_count +=1
            elif str(row['Sentiment']).lower().replace(' ','') == 'negative':
                neg_count += 1
                total_count += 1
            else:
                neu_count += 1
                total_count += 1
        
        
        pos_share = pos_count/total_count
        neg_share = neg_count/total_count
        neu_share = neu_count/total_count
        new_row = {'Month': date,
        'Percentage Positive': pos_share,
        'Percentage Negative': neg_share,
        'Percentage Neutral': neu_share}

        df_count = df_count._append(new_row, ignore_index = True)


df_count = df_count.sort_values(by='Month')
plt.plot(df_count['Month'], df_count['Percentage Positive'])
plt.plot(df_count['Month'], df_count['Percentage Negative'])
plt.plot(df_count['Month'], df_count['Percentage Neutral'])

plt.xlabel('Year')
plt.ylabel('Percentage of Articles')
plt.title('Sentiment Analysis')
plt.legend(['Positive','Negative','Neutral'])
plt.savefig(f'/Users/LindaSong/Desktop/{str(method)}plot 6.png')