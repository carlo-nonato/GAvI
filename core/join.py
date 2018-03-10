import glob
import os

from .utils import *

def join(files, output_file):
    """Joins multiple tweets binary files"""
    
    tweets = []
    for filename in sorted(files, key=os.path.getmtime):
        tweets.extend(load_tweets(filename))
    dump_tweets(tweets, output_file)
    
if __name__ == '__main__':
    import argparse as ap

    argparser = ap.ArgumentParser(description=join.__doc__)
    argparser.add_argument('files', nargs='+')
    argparser.add_argument('-o', dest='output_file', default='joined')
    args = argparser.parse_args()
    join(args.files, args.output_file)
