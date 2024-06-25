import ssl
import certifi
import nltk

# Update SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Download the vader_lexicon
nltk.download('all')