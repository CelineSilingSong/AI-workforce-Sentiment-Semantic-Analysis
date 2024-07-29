# Sentiment Analysis News Article

import nltk
import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import ssl
import certifi


# Update SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# lemmatize the tokens
lemmatizer = WordNetLemmatizer()
# a function to preprocess the text:
def preprocess_text(text):
    # removing the name of the publisher
    index = text.find('-')
    if index != -1:
        text = text[:index]
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # removing stop words
    filtered_tokens = []
    for token in tokens:
        if token not in stopwords.words('english'):
            filtered_tokens.append(token)
    lemmatized_tokens = []
    for token in filtered_tokens:
        lemmatized_tokens.append(lemmatizer.lemmatize(token))
    
    # Join the tokens into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

# Defining a function to analyze the sentiment
analyzer = SentimentIntensityAnalyzer()
def Return_Score(text):
    scores = analyzer.polarity_scores(text)
    return scores

def Return_Sentiment(scores):
    positivity = scores['pos']
    negativity = scores['neg']
    neutrality = scores['neu']

    if positivity == negativity:
        sentiment = 'Neutral'
    else:
        if positivity > negativity:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'

    return sentiment

directory = '/Users/LindaSong/Desktop/AI job 3'

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # constructing full path
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        # preprocessing every title
        df['Preprocessed Title'] = df['Title'].apply(preprocess_text)
        df['Value'] = df['Preprocessed Title'].apply(Return_Score)
        df['Sentiment'] = df['Value'].apply(Return_Sentiment)
        df.to_csv(f'/Users/LindaSong/Desktop/AI Sentiment Results 3/sentiment analyzed {filename}')

