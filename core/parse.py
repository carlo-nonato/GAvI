import itertools as it
import re

from .utils import get_io_args, dump_tweets
from .tweet import Tweet

def parse(filename):
    """Parses the tweets and returns a list of tweets objects"""

    # Pattern used to split the file in single tweet's block of
    # information. A block is identified by two newline characters
    # followed by a field or by the end of the string.
    split_pattern = re.compile(r'\n\n(?=[A-z_-]+ : |\Z)')
    # Pattern used to extract fields and their content.
    # The field matches every character before the colon.
    # The content matches every character until the next field or the end
    # of the string.
    fields_pattern = re.compile(r'(^.*?) : (.+?)(?=\n+[A-z_-]+ : |\Z)',
                                re.MULTILINE | re.DOTALL)

    # parse every tweet and make them dict-like objects
    all_tweets = [] # original representation
    with open(filename) as in_file:
        for tweet_info in split_pattern.split(in_file.read()):
            tweet = Tweet(fields_pattern.findall(tweet_info))
            if tweet:
                all_tweets.append(tweet)

    # group retweets togheter (original tweet -> retweets)
    tweets = [] # final representation
    tweet_key = lambda tweet: (tweet.created_at_author,
                               tweet.username_author,
                               tweet.text)
    all_tweets = sorted(all_tweets, key=tweet_key)
    for _, group in it.groupby(all_tweets, key=tweet_key):
        tweet = next(group) # first one is the retweets leader
        tweet.retweets = list(group)
        tweets.append(tweet)

    return tweets

if __name__ == "__main__":
    import argparse as ap

    argparser = ap.ArgumentParser(description=parse.__doc__)
    args = get_io_args(argparser)
    dump_tweets(parse(args.input_file), args.output_file)
