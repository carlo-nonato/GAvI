from nltk.sentiment.vader import SentimentIntensityAnalyzer
from math import log10
import matplotlib.pyplot as plt

from .utils import *
from .exhibitions import TITLES

sia = SentimentIntensityAnalyzer()

def share(tweet):
    return (tweet.retweet_count*3 + tweet.favorited_count + 1)**(1/4)
##           if tweet.is_retweet() else 1

def polarity(tweet):
    return sia.polarity_scores(tweet.text.replace('#', ''))['compound']

def is_neutral(polarity):
    return -0.5 < polarity < 0.5

def sentiment_history(tweet):
    history = []
    old_share = 0
    pol = polarity(tweet)
    # Damps the effect of neutral tweets
    if is_neutral(pol):
        f = lambda x: log10(x + 1)
    else:
        f = lambda x: x
        
    for t in tweet.self_and_retweets():
        new_share = f(share(t))
        history.append([t.created_at, pol, old_share, new_share])
        old_share = new_share
    return history

def sentiment(tweets, exhibition):
    """Compute the sentiment values of a particular exhibition"""

    tweets = group_by_exhibition(tweets)[exhibition]
    full_history = []
    num, den = 0, 0
    dates, sentiment_values = [], []
    # Gather all tweets and retweets' polarity and share information
    # in a single list 
    for tweet in tweets:
        full_history.extend(sentiment_history(tweet))
    # Sort history points by date and for every point compute the new
    # sentiment value
    for history_point in sorted(full_history, key=lambda x: x[0]):
        date, pol, old_share, new_share = history_point
        num -= old_share*pol
        den -= old_share
        num += new_share*pol
        den += new_share
        dates.append(date)
##        print((str(date), pol, old_share, new_share), num/den)
        sentiment_values.append(num/den)
    return dates, sentiment_values

def sentiment_plot(tweets, exhibition):
    """Plot sentiment values of an exhibition over time"""
    
    dates, sentiment_values = sentiment(tweets, exhibition)
    plt.subplot(2, 1, 1)
    plt.title(TITLES[exhibition] + ' - Sentiment')
    plt.stem(dates, sentiment_values, markerfmt='.')
    plt.plot(dates, sentiment_values, '--')
    plt.ylim(-1, 1)
    if len(dates) > 1:
        plt.xlim(dates[0], dates[-1])
    plt.annotate('{:0.2f}'.format(sentiment_values[-1]),
                 xy=(1, sentiment_values[-1]),
                 xytext=(5, 0),
                 xycoords=('axes fraction', 'data'),
                 textcoords='offset points')

def popularity_plot(tweets, exhibition):
    tweets = group_by_exhibition(tweets)[exhibition]

    plt.subplot(2, 1, 2)
    history = []
    dates = []
    total_retweets, total_favorited = 0, 0
    total_retweets_values = []
    total_favorited_values = []
    for tweet in tweets:
        history.extend(tweet.self_and_retweets())
    for tweet in sorted(history, key=lambda x: x.created_at):
        dates.append(tweet.created_at)
        total_retweets += tweet.retweet_count
        total_favorited += tweet.favorited_count
        total_retweets_values.append(total_retweets)
        total_favorited_values.append(total_favorited)
    plt.title(TITLES[exhibition] + ' - Popularity')
    plt.plot(dates, total_retweets_values, '.-', label='retweets')
    plt.plot(dates, total_favorited_values, '.-', label='favorited')
    if len(dates) > 1:
        plt.xlim(dates[0], dates[-1])
    plt.legend()
    plt.annotate(str(total_retweets_values[-1]),
                 xy=(1, total_retweets_values[-1]),
                 xytext=(5, 0),
                 xycoords=('axes fraction', 'data'),
                 textcoords='offset points')
    plt.annotate(str(total_favorited_values[-1]),
                 xy=(1, total_favorited_values[-1]),
                 xytext=(5, 0),
                 xycoords=('axes fraction', 'data'),
                 textcoords='offset points')

if __name__ == "__main__":
    import argparse as ap
    
    argparser = ap.ArgumentParser(description=sentiment_plot.__doc__)
    argparser.add_argument('input_file')
    argparser.add_argument('exhibition', type=int)
    args = argparser.parse_args()
    tweets = load_tweets(args.input_file)
    sentiment_plot(tweets, args.exhibition)
    popularity_plot(tweets, args.exhibition)
    plt.subplots_adjust(left=0.05, top=0.95, bottom=0.05, right=0.95)
    plt.show()
