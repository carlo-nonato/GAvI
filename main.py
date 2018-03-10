import matplotlib.pyplot as plt

from core.utils import *
from core.sentiment import *
from core.tagging_pie_chart import *
    
def main():
    return group_by_exhibition(load_tweets('out/mostre_tagged'))[2]
    
if __name__ == '__main__':
##    from time import time
##    start = time()
    tweets = main()
##    print(time() - start)
