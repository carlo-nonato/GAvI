from datetime import datetime
import re
from googletrans import Translator

from . import fields

UNKNOWN_LANG = 'und'
AUTO_LANG = 'auto'

class TweetText(str):
    """Class that represents the text of a tweet.
       Removes RTs headings and compares dealing with truncations"""

    text_pattern = re.compile('((?:RT \S*: )*)(.*)', re.DOTALL)

    def __new__(cls, text):
        match = cls.text_pattern.match(text.rstrip('…'))
        headings, text = match.group(1, 2)
        obj = str.__new__(cls, text)
        obj.headings = headings
        return obj

    def __eq__(self, other):
        return self.startswith(other) or other.startswith(self)

class Tweet(dict):
    """Dict-like class that represents a tweet"""
    
    # matches every character c such that ord(c) > 65535
    # BMP stays for Basic Multilingual Plane
    non_bmp_pattern = re.compile('[^\u0000-\uFFFF]')
    translator = Translator()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._created_at = None
        self._text = ''
        self._username = ''
        self.retweets = []

    @property
    def created_at(self):
        if not self._created_at:
            created_at = self.get(fields.CREATED_AT_AUTHOR,
                                  self[fields.CREATED_AT])
            self._created_at = datetime.strptime(created_at,
                                                 '%a %b %d %X %z %Y')
        return self._created_at

    @property
    def username(self):
        if not self._username:
            self._username = self.get(fields.USERNAME_AUTHOR,
                                      self[fields.USERNAME])
        return self._username

    @property
    def text(self):
        if not self._text:
            self._text = TweetText(self[fields.TEXT])
        return self._text

    def translate(self, lang):
        if self[fields.LANG] == lang:
            return

        text = self.non_bmp_pattern.sub('', self[fields.TEXT])
        src_lang = (self[fields.LANG]
                    if self[fields.LANG] != UNKNOWN_LANG else AUTO_LANG)
        self._text = TweetText(self.translator.translate(text,
                                                         src=src_lang,
                                                         dest=lang).text)

    def text_with_headings(self):
        return self.text.headings + self.text

    def retweet_count(self):
        if not self.retweets:
            return 0
        return int(self.retweets[-1][fields.RETWEET_COUNT])

    def favorited_count(self):
        if not self.retweets:
            return 0
        return int(self.retweets[-1][fields.FAVORITED_COUNT])
