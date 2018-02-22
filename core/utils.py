import pickle
import os
from functools import wraps

def write_tweets(tweets, filename):
    with open(filename, 'w') as out_file:
        for tweet in tweets:
            for field, content in tweet.items():
                out_file.write(field + ' : ' + str(content) + '\n')
            out_file.write('\n')

def dump_tweets(tweets, filename):
    """Dump tweets to a binary file"""
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as out_file:
        pickle.dump(tweets, out_file, pickle.HIGHEST_PROTOCOL)

def load_tweets(filename):
    """Load tweets from a binary file"""

    tweets = []
    with open(filename, 'rb') as in_file:
        tweets = pickle.load(in_file)
    return tweets

def get_io_args(argparser, output_suffix=''):
    argparser.add_argument('input_file')
    argparser.add_argument('-o', dest='output_file')
    args = argparser.parse_args()
    if not args.output_file:
        args.output_file = os.path.splitext(args.input_file)[0]+output_suffix
    return args
    
if __name__  == '__main__':
    import argparse as ap
    
    argparser = ap.ArgumentParser(description="Write tweets to a text file")
    args = get_io_args(argparser, '.txt')
    write_tweets(load_tweets(args.input_file), args.output_file)
