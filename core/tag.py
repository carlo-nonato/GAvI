import re
from nltk.corpus import stopwords

from .utils import get_io_args, load_tweets, dump_tweets
from . import fields

DEFAULT_EXHIBITIONS_FILE = 'txt/exhibitions.txt'
EN_STOPWORDS = stopwords.words('english')

def read_exhibitions(filename):
    exhibitions = []
    words_pattern = re.compile('\w+')

    with open(filename) as in_file:
        for line in in_file:
            exhibition = []
            for part in line.strip().lower().split(' : '):
                exhibition.append([word for word in words_pattern.findall(part)
                                   if word not in EN_STOPWORDS])
            exhibitions.append(exhibition)

    return exhibitions

def tag(tweets, exhibitions_file=DEFAULT_EXHIBITIONS_FILE):
    """Tries to tag each tweet with one exhibition"""

    exhibitions = read_exhibitions(exhibitions_file)
    out_tweets = []
    matched = False
    for tweet in tweets:
        text = tweet.text.lower()
        tweet.exhibition = ''
        for place_tokens, name_tokens in exhibitions:
            place_similarity = (sum(x in text for x in place_tokens)/
                                len(place_tokens))
            name_similarity = (sum(x in text for x in name_tokens)/
                               len(name_tokens))
            if place_similarity*name_similarity > 0:
                tweet.exhibition += (' '.join(name_tokens) + ' ',
                                    str(place_similarity) + ', ' +
                                    str(name_similarity))
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
