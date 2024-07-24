# Semantic analysis and Sentiment analysis (English Version):
import os
import pandas as pd

# preprocessor block:
Directory = 'en-macroed'

files = []
for file in os.listdir(Directory):
    if file.endswith('.csv'):
        file_path = os.path.join(Directory,file)
        files.append(file_path)

sorted_files = sorted(files)

for file in sorted_files:
    df = pd.read_csv(file)
    


# Semantic analysis block:
from bertopic import BERTopic




# Sentiment analysis block:




# cleaning the dataset:
