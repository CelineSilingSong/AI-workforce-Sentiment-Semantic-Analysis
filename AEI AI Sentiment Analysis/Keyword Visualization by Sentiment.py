# Keyword Visualization by Sentiment

import os
import pandas as pd
from LanguageAnalyzer import keywordExtractor
from collections import Counter

# visualization for flair:

keywordextractor = keywordExtractor()

Directory = 'flair-sentiment-en'

files = []
for file in os.listdir(Directory):
    if file.endswith('.csv'):
        file_path = os.path.join(Directory,file)
        files.append(file_path)

sorted_files = sorted(files)

# conducting keyword analysis

# compiling articles according to sentiment
compiled_positive_list = []
compiled_negative_list = []
overall_keyword_freq = Counter()

for file in sorted_files:
    df = pd.read_csv(file)
    positive_article_list = []
    negative_article_list = []
    for row in df.iterrows():
        if row[1]['Sentiment'] == 'positive':
            positive_article_list.append(str(row[1]['Preprocessed Text']))
        else:
            negative_article_list.append(str(row[1]['Preprocessed Text']))
    compiled_positive_list.extend(positive_article_list)
    compiled_negative_list.extend(negative_article_list)
    for article in df['Preprocessed Text'].astype(str):
      overall_keyword_freq.update(article.split())

exclude_phrase = ['artificial intelligence', 'ai', 'u', 'artificial', 'intelligence', 'generative', 'work', 'nan', 'could', 'many', 'may', 'say','used', 'one', 'like']
positive_graph = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/keyword by sentiment/flair positive.png'
negative_graph = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/keyword by sentiment/flair negative.png'
keywordextractor.visualize_key_concept_sklearn_without_common(compiled_positive_list, exclude_phrase, positive_graph, overall_keyword_freq)
keywordextractor.visualize_key_concept_sklearn_without_common(compiled_negative_list, exclude_phrase, negative_graph, overall_keyword_freq)


# spacy:
# keywordextractor = keywordExtractor()
# 
# Directory = 'ex-sentiment-en'
# 
# files = []
# for file in os.listdir(Directory):
#     if file.endswith('.csv'):
#         file_path = os.path.join(Directory,file)
#         files.append(file_path)
# 
# sorted_files = sorted(files)
# 
# # conducting keyword analysis
# 
# # compiling articles according to sentiment
# compiled_positive_list = []
# compiled_negative_list = []
# compiled_neutral_list = []
# overall_keyword_freq = Counter()
# 
# for file in sorted_files:
#     df = pd.read_csv(file)
#     positive_article_list = []
#     negative_article_list = []
#     neutral_article_list = []
#     for row in df.iterrows():
#         if row[1]['Sentiment'] == 'positive':
#             positive_article_list.append(str(row[1]['Preprocessed Text']))
#         elif row[1]['Sentiment'] == 'negative':
#             negative_article_list.append(str(row[1]['Preprocessed Text']))
#         else:
#             neutral_article_list.append(str(row[1]['Preprocessed Text']))
#     compiled_positive_list.extend(positive_article_list)
#     compiled_negative_list.extend(negative_article_list)
#     compiled_neutral_list.extend(neutral_article_list)
#     for article in df['Preprocessed Text'].astype(str):
#         overall_keyword_freq.update(article.split())
# 
# exclude_phrase = ['artificial intelligence', 'ai', 'u', 'artificial', 'intelligence', 'generative', 'work', 'nan', 'could', 'many', 'use','way', 'year', 'make', 'one', 'used']
# positive_graph = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/keyword by sentiment/spacy positive.png'
# negative_graph = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/keyword by sentiment/spacy negative.png'
# neutral_graph =  '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/keyword by sentiment/spacy neural.png'
# keywordextractor.visualize_key_concept_sklearn_without_common(compiled_positive_list, exclude_phrase, positive_graph, overall_keyword_freq)
# keywordextractor.visualize_key_concept_sklearn_without_common(compiled_negative_list, exclude_phrase, negative_graph, overall_keyword_freq)
# keywordextractor.visualize_key_concept_sklearn_without_common(compiled_neutral_list, exclude_phrase, neutral_graph, overall_keyword_freq)