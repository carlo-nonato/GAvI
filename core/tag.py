import re
from nltk.corpus import stopwords

from .utils import get_io_args, load_tweets, dump_tweets
from . import fields, exhibitions

def similarity(weighted_tokens, text):
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
    matched = False
    for tweet in tweets:
        text = tweet.text_with_headings().lower()
        tweet.exhibition = ''
        for place, content in zip(exhibitions.places, exhibitions.contents):
            place_similarity = similarity(place, text)
            content_similarity = similarity(content, text)
            if place_similarity*content_similarity > 0.2:
                tweet.exhibition += (' '.join(str(x) for x in place) + ' ' +
                                     str(place_similarity) + ' * ' +
                                     str(content_similarity) + ' = ' +
                                     str(place_similarity*content_similarity))
                matched = True
        if matched:
            out_tweets.append(tweet)
            matched = False
    return out_tweets

if __name__ == "__main__":
    import argparse as ap

    argparser = ap.ArgumentParser(description=tag.__doc__)
    args = get_io_args(argparser, '_tagged')
    dump_tweets(tag(load_tweets(args.input_file)), args.output_file)
