import os
import pandas as pd
from LanguageAnalyzer import SemanticAnalyser
from LanguageAnalyzer import keywordExtractor

# visualizing keyword for every month

directory = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/preprocessed-en'
keywordextractor = keywordExtractor()
exclude_phrase = ['artificial intelligence', 'ai', 'u', 'artificial', 'intelligence', 'generative', 'work','job', 'nan', 'could']

for filename in os.listdir(directory):

    if filename.endswith('.csv'):
        file = str(filename).replace('.csv','')
        file_path = os.path.join(directory,filename)
        df = pd.read_csv(file_path)
        article_list = df['Preprocessed Text'].astype(str).to_list()

        graph_path = (f'/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/wordnet-en/{file}.png')
        
        keywordextractor.visualize_key_concept_sklearn_2(article_list, exclude_phrase, graph_path)




