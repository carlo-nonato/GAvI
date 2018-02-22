import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import itertools as it
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from core.utils import *
from core import fields

sia = SentimentIntensityAnalyzer()

def share(tweet):
    return (int(tweet[fields.RETWEET_COUNT]),
            int(tweet[fields.FAVORITED_COUNT]))

def foo(tweet, polarity):
    return (tweet[fields.CREATED_AT],
            share(tweet) if tweet.is_retweet() else (0, 0),
            polarity)
    
def main():
    tweets = load_tweets('out/mostre_translated_0')
    print(len(tweets))
    return tweets

##    out = []
##    exhibition_key = lambda x: x.exhibition
##    tweets = sorted(tweets, key=exhibition_key)
##    for exh, group in it.groupby(tweets, key=exhibition_key):
##        if exh != 9:
##            continue
##
##        y = []
##        for tweet in group:
##            out.append(tweet)
##            polarity = sia.polarity_scores(tweet.text_with_headings()
##                                           )['compound']
##            y.append(foo(tweet, polarity))
##            for rt in tweet.retweets:
##                y.append(foo(rt, polarity))
##    
##    print(y)
##    return out
##    print(np.power(y, 2))
##    fig, (ax1, ax2) = plt.subplots(1, 2)
##    ax1.plot(y, '.-')
##    ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
##    ax2.plot(np.power(y, 2), '.-')
##    ax2.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
##    plt.show()
    
##    with open('out/tag.txt', 'w') as f:
##        for tweet in tweets:
##            f.write('TEXT: ' + tweet.text.with_headings() + '\n')
##            f.write('HASHTAGS: ' + ' '.join(tweet.hashtags) + '\n')
##            f.write('EXHIBITION: ' + str(tweet.exhibition) + '\n\n')

##    tweets = load_tweets('out/mostre')
##    with open('out/mostre.txt', 'w') as f:
##        for tweet in tweets:
##            f.write('TEXT: ' + tweet[fields.TEXT] + '\n')
##            f.write('HASHTAGS: ' + ' '.join(tweet.hashtags) + '\n\n')

if __name__ == '__main__':
##    from time import time
##    start = time()
    tweets = main()
##    print(time() - start)
