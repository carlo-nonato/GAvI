from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer
from nltk.classify import NaiveBayesClassifier

##from .utils import *
##from . import fields

def tokenize(text):
    tokenizer = TweetTokenizer()
    tokens = []
    for word in tokenizer.tokenize(text.lower()):
        if word.startswith('@') or word.startswith('http'):
            continue
        tokens.append(word)
    return tokens

def format_sentence(sentence):
    return({word: True for word in tokenize(sentence)})

def sentiment():
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    pos = [[format_sentence(tweet), 'pos'] for tweet in positive_tweets]
    neg = [[format_sentence(tweet), 'neg'] for tweet in negative_tweets]
    training = pos + neg
    classifier = NaiveBayesClassifier.train(training)
    return classifier

if __name__ == "__main__":
    c = sentiment()
