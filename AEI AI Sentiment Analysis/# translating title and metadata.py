# translating title and metadata
# by Siling Song

import os
import pandas as pd
from googletrans import Translator
import re

translator = Translator()

directory = 'the directory path'

files = []
for file in os.listdir(directory):
    if file.endswith('csv'):
        file_path = os.path.join(directory,file)
        files.append(file_path)

sorted_files = sorted(files)

for file in sorted_files:
    df = pd.read_csv(file)
    file_name = os.path.basename(file)
    match = re.match(r'^([a-zA-Z]{2})-', file_name)
    if match:
        language_code = match.group(1)
        print(f"language code extracted: {language_code}")
    else:
        print(f'failure to extract language code for file {file_name}')
    
    data_translated = {
        'URL Link':[],
        'Title Translated':[],
        'Description Translated':[],
        'Date':[],
        'Source':[],
        'Source Link':[],
        'Original Title':[],
        'Original Description':[] }
    
    for row in df.iterrows():
        url = row[1]['URL link']
        title = row[1]['Title']
        date = row[1]['Date']
        source = row[1]['Source']
        source_link = row[1]['Source Link']

        max_length = 0
        max_descr = 'NA'
        # geeting the longest description
        for column_name in df.columns:
            if 'description' in column_name:
                description_length = len(row[1][column_name])
                if description_length > max_length:
                    max_length = description_length
                    max_descr = row[1][column_name]

        translated_description = translator.translate(max_descr).text
        translated_title = translator.translate(title).text

        data_translated['URL Link'].append(url)
        data_translated['Title Translated'].append(translated_title)
        data_translated['Description Translated'].append(translated_description)
        data_translated['Date'].append(date)
        data_translated['Source'].append(source)
        data_translated['Source Link'].append(source_link)
        data_translated['Original Title'].append(title)
        data_translated['Original Description'].append(max_descr)
    
    translated_df = pd.DataFrame(data_translated, index = False)

    translated_df.to_csv('output path')

