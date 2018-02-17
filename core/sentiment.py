from nltk.sentiment.vader import SentimentIntensityAnalyzer

from .utils import *
from . import match, fields

DEFAULT_INPUT_FILE = match.DEFAULT_OUTPUT_FILE
DEFAULT_OUTPUT_FILE = 'out/sentiment'
DEFAULT_OUTPUT_TXT_FILE = 'out/sentiment.txt'

@optional_input(DEFAULT_INPUT_FILE)
@optional_output(DEFAULT_OUTPUT_FILE, DEFAULT_OUTPUT_TXT_FILE)
def sentiment(tweets):
    """Basic sentiment analysis"""

    sia = SentimentIntensityAnalyzer()
    
    for tweet in tweets:
        tweet['polarity'] = sia.polarity_scores(tweet[fields.TEXT])

    return tweets

if __name__ == "__main__":
    import argparse as ap

    argparser = ap.ArgumentParser(description=sentiment.__doc__)
    add_io_argparser(argparser, DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE,
                     DEFAULT_OUTPUT_TXT_FILE)
    args = argparser.parse_args()

    sentiment(input_file=args.input_file,
              output_file=args.output_file,
              txt_file=args.txt_file)
