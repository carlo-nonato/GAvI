import matplotlib.pyplot as plt

from .utils import load_tweets, group_by_exhibition
from .exhibitions import TITLES

def tagging_pie_chart(tweets):
    """Plot a pie chart with tagging results"""

    exh_to_tweets = group_by_exhibition(tweets)
    labels = []
    values = []
    for exhibition, tweets in exh_to_tweets.items():
        labels.append(TITLES[exhibition])
        values.append(len(tweets))
    # Display absolute numbers on the wedges
    total = sum(values)
    autopct = lambda x: '{:.0f}'.format(x*total/100)
    # Set axis with the same scale
    plt.axis('equal')
    # Plot the pie chart
    wedges, texts, autotexts = plt.pie(values,
                                       startangle=90,
                                       wedgeprops={'linewidth': 1,
                                                   'edgecolor': 'black'},
                                       autopct=autopct,
                                       pctdistance=0.8)
    # Set the style of the wedges numbers
    for autotext in autotexts:
        autotext.set_family('Open Sans')
        autotext.set_fontsize(12)
        autotext.set_color('white')
    # Legend
    plt.legend(labels,
               loc='center right',
               bbox_to_anchor=(1, 0.5),
               bbox_transform=plt.gcf().transFigure,
               prop={'family':'Open Sans', 'size': 12})
    plt.subplots_adjust(left=0, bottom=0, right=0.7, top=1)
    plt.show()

if __name__ == '__main__':
    import argparse as ap

    argparser = ap.ArgumentParser(description=tagging_pie_chart.__doc__)
    argparser.add_argument('input_file')
    args = argparser.parse_args()
    tagging_pie_chart(load_tweets(args.input_file))
