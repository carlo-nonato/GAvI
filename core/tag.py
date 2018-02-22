import re
from nltk.corpus import stopwords

from .utils import get_io_args, load_tweets, dump_tweets
from .exhibitions import PLACES, CONTENTS, HASHTAGS
from . import fields

THRESHOLD = 0.3

def similarity(weighted_tokens, text):
    """Compute the similarity between weighted tokens dictionary and a
       string"""
    
    sim = 0
    for token, weight in weighted_tokens.items():
        if isinstance(token, tuple):
            sim += any(t in text for t in token)*weight
        else:
            sim += (token in text)*weight
    return min(sim, 1)

def tag(tweets):
    """Tries to tag each tweet with one exhibition"""

    out_tweets = []
    for tweet in tweets:
        # headings contain username informations. Museums can be cited here.
        text = tweet.text.with_headings().lower()
        # search for a match with one exhibition
        for exh, (place, content, hashtags) in enumerate(zip(PLACES,
                                                             CONTENTS,
                                                             HASHTAGS)):
            place_similarity = similarity(place, text)
            content_similarity = similarity(content, text)
            # if one of the hashtags is found or if threshold is exceeded:
            # tag the tweet and go to te next one
            if (any(hashtag in tweet.hashtags for hashtag in hashtags)) or \
                   (place_similarity*content_similarity > THRESHOLD):
                tweet.exhibition = exh
                out_tweets.append(tweet)
                break

    return out_tweets

if __name__ == "__main__":
    import argparse as ap

    argparser = ap.ArgumentParser(description=tag.__doc__)
    args = get_io_args(argparser, '_tagged')
    dump_tweets(tag(load_tweets(args.input_file)), args.output_file)
