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

##class optional_value_decorator:
##    def __init__(self, arg_name, default_value=None):
##        self.arg_name = arg_name
##        self.default_value = default_value
##
##    def __call__(self, function):
##        self.function = function
##        @wraps(function)
##        def decorator(*args, **kwargs):
##            self.value = self._get_value(kwargs)
##            return self.handler(*args, **kwargs)
##        return decorator
##
##    def _get_value(self, kwargs):
##        self.value = kwargs.pop(self.arg_name, None)
##        if self.value is True:
##            if self.default_value is None:
##                raise ValueError
##            return self.default_value
##        return self.value
##
##class tweets_input(optional_value_decorator):
##    """Decorates the function so it can read tweets from an input file"""
##    def __init__(self, default_input_file=None):
##        super().__init__('input_file', default_input_file)
##
##    def handler(self, *args, **kwargs):
##        if self.value is not None:
##            args = (load_tweets(self.get_value()), args[1:])
##        return self.function(*args, **kwargs)
##
##class tweets_output(optional_value_decorator):
##    """Decorates the function so it can write tweets to an output file"""
##    
##    output_func = None
##    
##    @classmethod
##    def with_output_func(cls, output_func):
##        output_func = staticmethod(output_func)
##        return type('tweets_output_f', (cls, ), {'output_func': output_func})
##    
##    def __init__(self, default_output_file):
##        super().__init__('output_file', default_output_file)
##
##    def handler(self, *args, **kwargs):
##        tweets = self.function(*args, **kwargs)
##        if self.value is not None:
##            self.output_func(tweets, self.value)
##        return tweets
##
##tweets_output_bin = tweets_output.with_output_func(dump_tweets)
##tweets_output_txt = tweets_output.with_output_func(write_tweets)

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
