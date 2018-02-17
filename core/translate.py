from .utils import get_io_args, load_tweets, dump_tweets

DEFAULT_LANG = 'en'

def translate(tweets, lang=DEFAULT_LANG):
    """Translates all the tweets to the same language"""

    out_tweets = []
    for tweet in tweets:
        try:
            tweet.translate(lang)
            out_tweets.append(tweet)
        except Exception as e:
            print(e)
            print(tweets.index(tweet), tweet)
    return out_tweets

if __name__ == '__main__':
    import argparse as ap

    argparser = ap.ArgumentParser(description=translate.__doc__)
    argparser.add_argument('-l', '--lang', default=DEFAULT_LANG,
                           help='destination language')
    argparser.add_argument('-c', '--chunk', type=int, help='chunk number')
    argparser.add_argument('-s', '--chunk-size', type=int, default=1000)
    args = get_io_args(argparser, '_translated')
    tweets = load_tweets(args.input_file)
    if args.chunk is not None:
        tweets = tweets[args.chunk*args.chunk_size:
                        (args.chunk+1)*args.chunk_size]
        args.output_file += '_' + str(args.chunk)
    dump_tweets(translate(tweets, args.lang), args.output_file)
