# Semantic analysis and Sentiment analysis (English Version Without Content):
import os
import pandas as pd

# preprocessor block:
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure you have the required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# A function to expand contractions
def expand_contractions(text):
    contractions = {
        "can't": "cannot",
        "won't": "will not",
        "n't": " not",
        "'re": " are",
        "'s": " is",
        "'d": " would",
        "'ll": " will",
        "'t": " not",
        "'ve": " have",
        "'m": " am"
    }
    for contraction, expanded in contractions.items():
        text = re.sub(contraction, expanded, text)
    return text

def preprocess_text_nltk(text):
    # Remove the publisher name
    text = text.split('-')[0].strip()
    
    # Expand contractions
    text = expand_contractions(text)
    
    # Remove URLs and email addresses
    text = re.sub(r'http\S+|www\S+|https\S+|@\S+', '', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove digits
    text = re.sub(r'\d+', '', text)
    
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    
    # Lemmatize tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Join tokens into a single string
    processed_text = ' '.join(lemmatized_tokens)
    
    return processed_text

# Keyword Extraction and visualization Block:
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def visualize_key_concept_sklearn(processed_articles):
    # Keywords Extraction
    # Flatten processed articles into strings
    flattened_articles = [" ".join(article) for article in processed_articles]
    vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000)
    X = vectorizer.fit_transform(flattened_articles)
    keywords = vectorizer.get_feature_names_out()

    # frequency analysis
    all_words = [word for article in processed_articles for word in article]
    word_counts = Counter(all_words)
    common_words = word_counts.most_common(20)  # Get the 20 most common words
    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(counts), y=list(words))
    plt.xlabel('Frequency')
    plt.ylabel('Keywords')
    plt.title('Top Keywords in News Articles')
    plt.show()

    # Wordcloud visualization:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Keywords')
    plt.show()

# Semantic analysis block:
from bertopic import BERTopic
topic_model = BERTopic()

def topic_clustering_bertopic(processed_articles):
    # Fit the model on the preprocessed articles
    topics, probabilities = topic_model.fit_transform(processed_articles)

    # Get the topic information
    topic_info = topic_model.get_topic_info()
    topics_dict = topic_model.get_topics()

    article_topics = []
    for topic in topics:
        topic_desc = topic_model.get_topic(topic)
        topic_words = ", ".join([word for word, _ in topic_desc])
        article_topics.append(topic_words)

    # Display results
    for i, topic in enumerate(article_topics):
        print(f"Article {i+1} is about: {topic}")



# Sentiment analysis block:
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
def Return_Score_nltk(processed_text):
    scores = analyzer.polarity_scores(processed_text)
    return scores

def Return_Sentiment_nltk(scores):
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

def Sentiment_analysis_nltk(processed_text):
    scores = analyzer.polarity_scores(processed_text)
    positivity = scores['pos']
    negativity = scores['neg']

    if positivity == negativity:
        sentiment = 'Neutral'
    else:
        if positivity > negativity:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'

    return scores,sentiment

from textblob import TextBlob
def Sentiment_analysis_textblob(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    binary_sentiment = 'positive' if sentiment > 0 else 'negative'
    return sentiment, binary_sentiment

from transformers import pipelines
def Sentiment_analysis_HFT(text):
    classifier = pipelines('sentiment-analysis')
    result = classifier(text)
    score = result['score']
    label = str(result['label']).lower()
    return score,label

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
# need to add these two to implementation code
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
def Sentiment_analysis_spacy(nlp, text):
    doc = nlp(text)
    score = doc._.blob.polarity
    binary_sentiment = 'positive' if score >0 else 'negative'
    return score, binary_sentiment




from flair.models import TextClassifier
from flair.data import Sentence

def Sentiment_analysis_flair(text):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(text)
    classifier.predict(sentence)
    label = sentence.labels[0]
    sentiment = 'positive' if label.value == 'POSITIVE' else 'negative'
    score = label.score
    return score,sentiment





# cleaning the dataset & implementation code:
Directory = 'en-macroed'

files = []
for file in os.listdir(Directory):
    if file.endswith('.csv'):
        file_path = os.path.join(Directory,file)
        files.append(file_path)

sorted_files = sorted(files)

for file in sorted_files:
    df = pd.read_csv(file)
    data_translated = {
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
        title = row[1]['Title']
        date = row[1]['Date']
        source = row[1]['Source']
        source_link = row[1]['Source Link']

        max_length = 0
        max_descr = 'NA'
        # geeting the longest description
        for column_name in df.columns:
            if 'description' in column_name:
                print(str(row[1][column_name]))
                description_length = len(str(row[1][column_name]))
                if description_length > max_length:
                    max_length = description_length
                    max_descr = row[1][column_name]
        