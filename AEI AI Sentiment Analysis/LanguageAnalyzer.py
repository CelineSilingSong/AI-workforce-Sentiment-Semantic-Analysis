# Semantic analysis and Sentiment analysis (English Version Without Content):
import os
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

from bertopic import BERTopic
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipelines
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from flair.models import TextClassifier
from flair.data import Sentence
from transformers import pipeline
from transformers import DistilBertTokenizer
import numpy as np
from collections import Counter

import torch
print(torch.backends.mps.is_available())
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

# preprocessor block:
class preprocessor:
    def __init__(self):
        # Initialize the lemmatizer
        self.lemmatizer = WordNetLemmatizer()

    # A function to expand contractions
    def expand_contractions(self, text):
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

    def preprocess_text_nltk(self, text):

        # Expand contractions
        text = self.expand_contractions(text)

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
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]

        # Join tokens into a single string
        processed_text = ' '.join(lemmatized_tokens)

        return processed_text

# Keyword Extraction and visualization Block:
class keywordExtractor:
    def __init__(self) -> None:
        pass
    
    def visualize_key_concept_sklearn(self, processed_articles, exclude_phrases):
        # Initialize exclude_phrases if not provided
        if exclude_phrases is None:
            exclude_phrases = []

        # Flatten processed articles into strings
        flattened_articles = [" ".join(article) for article in processed_articles]
        print(flattened_articles)

        # Initialize TfidfVectorizer to get unigrams and bigrams
        vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000, ngram_range=(1, 2))
        X = vectorizer.fit_transform(flattened_articles)
        keywords = vectorizer.get_feature_names_out()

        # Frequency analysis for unigrams and bigrams
        # Split each article into words and create a list of ngrams
        all_ngrams = [ngram for article in flattened_articles for ngram in article.split()]

        # Count the frequency of each ngram
        ngram_counts = Counter(all_ngrams)

        # Filter out specific phrases
        filtered_ngrams = {ngram: count for ngram, count in ngram_counts.items() if ngram not in exclude_phrases}

        # Optional: Filter out long phrases (e.g., keep only unigrams and bigrams)
        filtered_ngrams = {ngram: count for ngram, count in filtered_ngrams.items() if len(ngram.split()) <= 2}

        # Get the 20 most common ngrams after filtering
        common_ngrams = sorted(filtered_ngrams.items(), key=lambda x: x[1], reverse=True)[:20]
        ngrams, counts = zip(*common_ngrams)

        # Bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(counts), y=list(ngrams))
        plt.xlabel('Frequency')
        plt.ylabel('Keywords')
        plt.title('Top Keywords in News Articles')
        plt.show()

        # Wordcloud visualization
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(filtered_ngrams)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Keywords')
        plt.show()


    def visualize_key_concept_sklearn_2(self, processed_articles, exclude_phrases, graph_path):
        # Initialize exclude_phrases if not provided
        if exclude_phrases is None:
            exclude_phrases = []

        # Flatten processed articles into strings
        flattened_articles = processed_articles
        print(flattened_articles)

        # Initialize TfidfVectorizer to get unigrams and bigrams
        vectorizer = TfidfVectorizer(max_df=0.7,max_features=10000, ngram_range=(1, 2))
        X = vectorizer.fit_transform(flattened_articles)
        keywords = vectorizer.get_feature_names_out()

        # Frequency analysis for unigrams and bigrams
        # Split each article into words and create a list of ngrams
        all_ngrams = [ngram for article in flattened_articles for ngram in article.split()]

        # Count the frequency of each ngram
        ngram_counts = Counter(all_ngrams)

        # Filter out specific phrases
        filtered_ngrams = {ngram: count for ngram, count in ngram_counts.items() if ngram not in exclude_phrases}

        # Optional: Filter out long phrases (e.g., keep only unigrams and bigrams)
        filtered_ngrams = {ngram: count for ngram, count in filtered_ngrams.items() if len(ngram.split()) <= 2}

        # Get the 20 most common ngrams after filtering
        common_ngrams = sorted(filtered_ngrams.items(), key=lambda x: x[1], reverse=True)[:20]
        ngrams, counts = zip(*common_ngrams)

        # Bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(counts), y=list(ngrams))
        plt.xlabel('Frequency')
        plt.ylabel('Keywords')
        plt.title('Top Keywords in News Articles')

        # Wordcloud visualization
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(filtered_ngrams)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Keywords')
        plt.savefig(graph_path)

    def visualize_key_concept_sklearn_without_common(self, processed_articles, exclude_phrases, graph_path, overall_keyword_freq):
        # Initialize exclude_phrases if not provided
        if exclude_phrases is None:
            exclude_phrases = []

        # Flatten processed articles into strings
        flattened_articles = processed_articles

        # Initialize TfidfVectorizer to get unigrams and bigrams
        vectorizer = TfidfVectorizer(max_df=0.7, max_features=10000, ngram_range=(1, 2))
        X = vectorizer.fit_transform(flattened_articles)

        # Frequency analysis for unigrams and bigrams
        all_ngrams = [ngram for article in flattened_articles for ngram in article.split()]
        ngram_counts = Counter(all_ngrams)

        # Filter out specific phrases
        filtered_ngrams = {ngram: count for ngram, count in ngram_counts.items() if ngram not in exclude_phrases}

        # Filter out common keywords by comparing with overall frequencies
        filtered_ngrams = {ngram: count for ngram, count in filtered_ngrams.items()
                           if ngram not in overall_keyword_freq or abs(overall_keyword_freq[ngram] - count) <= 300}

        # Optional: Filter out long phrases (e.g., keep only unigrams and bigrams)
        filtered_ngrams = {ngram: count for ngram, count in filtered_ngrams.items() if len(ngram.split()) <= 2}

        # Get the 20 most common ngrams after filtering
        common_ngrams = sorted(filtered_ngrams.items(), key=lambda x: x[1], reverse=True)[:20]
        ngrams, counts = zip(*common_ngrams)

        # Bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(counts), y=list(ngrams))
        plt.xlabel('Frequency')
        plt.ylabel('Keywords')
        plt.title('Top Keywords in News Articles')

        # Wordcloud visualization
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(filtered_ngrams)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Keywords')
        plt.savefig(graph_path)

# positive & negative keyword wordcloud

class SemanticAnalyser:
    def __init__(self):
        self.topic_model = BERTopic()

    def topic_clustering_bertopic(self,processed_articles):
        # Fit the model on the preprocessed articles
        topics, probabilities = self.topic_model.fit_transform(processed_articles)

        # Get the topic information
        topic_info = self.topic_model.get_topic_info()
        topics_dict = self.topic_model.get_topics()

        article_topics = []
        for topic in topics:
            topic_desc = self.topic_model.get_topic(topic)
            topic_words = ", ".join([word for word, _ in topic_desc])
            article_topics.append(topic_words)

        # Display results
        for i, topic in enumerate(article_topics):
            print(f"Article {i+1} is about: {topic}")



class SentimentAnalyser:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer() 
        self.nlp = spacy.load('en_core_web_sm')
        self.classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english', revision='main',device = device)
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
        self.flair_classifier = TextClassifier.load('en-sentiment')


    def Return_Score_nltk(self,processed_text):
        scores = self.analyzer.polarity_scores(processed_text)
        return scores

    def Return_Sentiment_nltk(self, scores):
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

    def Sentiment_analysis_nltk(self,processed_text):
        scores = self.analyzer.polarity_scores(processed_text)
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

    def Sentiment_analysis_textblob(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            label = 'positive'
        elif sentiment == 0:
            label = 'neutral'
        else:
            label = 'negative'
        return sentiment, label

    
    def Sentiment_analysis_HFT(self, text):
        max_length = self.tokenizer.model_max_length
        tokens = self.tokenizer.tokenize(text)
        chunks = [tokens[i:i+max_length] for i in range(0, len(tokens), max_length)]
        
        results = []
        for chunk in chunks:
            chunk_text = self.tokenizer.convert_tokens_to_string(chunk)
            inputs = self.tokenizer(chunk_text, return_tensors="pt", truncation=True, padding=True)
            result = self.classifier.model(**inputs)
            logits = result.logits
            predicted_class_id = logits.argmax().item()
            labels = self.classifier.model.config.id2label
            label = labels[predicted_class_id]
            score = logits[0, predicted_class_id].item()
            results.append((score, label.lower()))
        
        # Aggregate results (e.g., average score or majority label)
        avg_score = np.mean([res[0] for res in results])
        # You might need to choose how to aggregate labels if necessary
        most_common_label = max(set([res[1] for res in results]), key=[res[1] for res in results].count)
        
        return avg_score, most_common_label

    def Sentiment_analysis_spacy(self,text):
        if 'spacytextblob' not in self.nlp.pipe_names:
            self.nlp.add_pipe('spacytextblob')
        doc = self.nlp(text)
        score = doc._.blob.polarity
        if score > 0:
            sentiment = 'positive'
        elif score == 0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'
        return score, sentiment


    def Sentiment_analysis_flair(self, text):
        sentence = Sentence(text)
        self.flair_classifier.predict(sentence)
        label = sentence.labels[0]
        sentiment = 'positive' if label.value == 'POSITIVE' else 'negative'
        score = label.score
        return score, sentiment