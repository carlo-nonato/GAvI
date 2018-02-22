from .utils import get_io_args, load_tweets, dump_tweets

DEFAULT_LANG = 'en'
DEFAULT_TRANSLATE_HASHTAGS = True

def translate(tweets,
              lang=DEFAULT_LANG,
              translate_hashtags=DEFAULT_TRANSLATE_HASHTAGS):
    """Translates all the tweets to the same language"""

    out_tweets = []
    for tweet in tweets:
        try:
            tweet.translate(lang, translate_hashtags)
            out_tweets.append(tweet)
        except Exception as e:
            print(e)
            print(tweets.index(tweet), tweet)

    return out_tweets

if __name__ == '__main__':
    import argparse as ap

    argparser = ap.ArgumentParser(description=translate.__doc__,
                                  formatter_class=ap.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-l', '--lang', default=DEFAULT_LANG,
                           help='destination language')
    argparser.add_argument('--preserve-hashtags', action='store_true',
                           help='doesn\'t translate hashtags')
    argparser.add_argument('-c', dest='chunk_number', type=int)
    argparser.add_argument('-s', dest='chunk_size', type=int, default=1000,
                           help='number of tweets to translate')
    args = get_io_args(argparser, '_translated')
    tweets = load_tweets(args.input_file)
    if args.chunk_number is not None:
        tweets = tweets[args.chunk_number*args.chunk_size:
                        (args.chunk_number+1)*args.chunk_size]
        args.output_file += '_' + str(args.chunk_number)
    dump_tweets(translate(tweets, args.lang, not args.preserve_hashtags),
                args.output_file)
