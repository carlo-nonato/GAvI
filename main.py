from core.utils import *
from core.parse import *
from core.translate import *
from core.tag import *
from core.tagging_pie_chart import *
from core.sentiment import *
    
def main():
    # This is only a usage example.
    # Real input is in 'txt/tweets.txt' but running with that large input may
    # result in exceptions because of translation library limits.
    
    tweets = parse('txt/test.txt')
    translated_tweets = translate(tweets)
    tagged_tweets = tag(tweets)
    tagging_pie_chart(tagged_tweets)
    # 2 is the exhibition id: 'Beyond Caravaggio'
    try:
        sentiment_popularity_plot(tagged_tweets, 2)
    except KeyError:
        print("No tagged tweets found. Try with another exhibition")
    
if __name__ == '__main__':
    main()
