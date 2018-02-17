import glob
import os

from .utils import *

def join(pathname, output_file):
    """Joins multiple binary files"""
    
    tweets = []
    for filename in sorted(glob.glob(pathname + '*'),
                           key=lambda x: os.path.getmtime(x)):
        tweets.extend(load_tweets(filename))
    dump_tweets(tweets, output_file)
    
if __name__ == '__main__':
    import argparse as ap

    argparser = ap.ArgumentParser(description=join.__doc__)
    argparser.add_argument('pathname')
    argparser.add_argument('output_file')
    args = argparser.parse_args()
    join(args.pathname, args.output_file)
