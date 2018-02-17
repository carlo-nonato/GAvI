from core.utils import *
from core import fields

def print_field(tweets, field):
    for tweet in tweets:
        print(tweet[field])
    
def main():
##    tweets = load_tweets('out/mostre_tagged')
##    with open('out/tag.txt', 'w') as f:
##        for tweet in tweets:
##            f.write(tweet.text + '\n')
##            f.write(tweet.exhibition + '\n\n')

    tweets = load_tweets('out/mostre')
    with open('out/mostre.txt', 'w') as f:
        for tweet in tweets:
            f.write('TEXT: ' + tweet.text + '\n\n')

if __name__ == '__main__':
    from time import time
    start = time()
    tweets = main()
    print(time() - start)
