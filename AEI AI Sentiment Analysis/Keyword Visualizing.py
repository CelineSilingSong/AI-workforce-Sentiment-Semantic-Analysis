# Keyword Visualizing
# Working Version

import os
import pandas as pd
from LanguageAnalyzer import preprocessor
from LanguageAnalyzer import keywordExtractor

Preprocessor = preprocessor()
keywordextractor = keywordExtractor()

# cleaning the dataset & implementation code:
Directory = 'reorganized-en'

files = []
for file in os.listdir(Directory):
    if file.endswith('.csv'):
        file_path = os.path.join(Directory,file)
        files.append(file_path)

sorted_files = sorted(files)

# conducting keyword analysis
compiled_list = []
for file in sorted_files:
    file_name = os.path.basename(file)
    df = pd.read_csv(file)
    data_to_process = {
        'URL Link':[],
        'Date':[],
        'Source':[],
        'Source Link':[],
        'Title':[],
        'Description':[],
        'Text to Process':[],
        'Preprocessed Text':[] }
    
    for row in df.iterrows():
        url = row[1]['URL link']
        title = row[1]['Title'].split('-')[0].strip()
        date = row[1]['Date']
        source = row[1]['Source']
        source_link = row[1]['Source Link']

        max_length = 0
        max_descr = 'NA'
        # getting the longest description
        for column_name in df.columns:
            if 'description' in column_name:
                description_length = len(str(row[1][column_name]))
                if description_length > max_length:
                    max_length = description_length
                    max_descr = str(row[1][column_name])
        text_to_preprocess = title + ' ' + max_descr
        text_to_preprocess = text_to_preprocess.replace('  ','')
        processed_text = Preprocessor.preprocess_text_nltk(text_to_preprocess)
    
        data_to_process['URL Link'].append(url)
        data_to_process['Date'].append(date)
        data_to_process['Source'].append(source)
        data_to_process['Source Link'].append(source_link)
        data_to_process['Title'].append(title)
        data_to_process['Description'].append(max_descr)
        data_to_process['Text to Process'].append(text_to_preprocess)
        data_to_process['Preprocessed Text'].append(processed_text)

    df = pd.DataFrame(data_to_process)
    # df.to_csv(f'preprocessed-en/{file_name}')

    article_list = df['Preprocessed Text'].to_list()
    compiled_list.append(article_list)

exclude_phrase = ['artificial intelligence', 'ai', 'u', 'artificial', 'intelligence', 'generative', 'work','job', 'nan', 'could', 'many']
keywordextractor.visualize_key_concept_sklearn(compiled_list, exclude_phrase)







