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

    def with_headings(self):
        return self.headings + self

class Tweet(dict):
    """Dict-like class that represents a tweet"""
    
    # matches every character c such that ord(c) > 65535
    # BMP stays for Basic Multilingual Plane
    non_bmp_pattern = re.compile('[^\u0000-\uFFFF]')
    hashtags_pattern = re.compile('#\w+')
    translator = Translator()
    date_format = '%a %b %d %X %z %Y' # Mon Jan 1 00:00:01 +0000 1970
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._created_at = None
        self._created_at_author = None
        self._text = ''
        self._hashtags = []
        self.retweets = []

    @property
    def created_at(self):
        if not self._created_at:
            self._created_at = datetime.strptime(self[fields.CREATED_AT],
                                                 self.date_format)
        return self._created_at

    @property
    def created_at_author(self):
        if not self._created_at_author:
            date_string = self.get(fields.CREATED_AT_AUTHOR,
                                   self[fields.CREATED_AT])
            self._created_at_author = datetime.strptime(date_string,
                                                        self.date_format)
        return self._created_at_author

    @property
    def username_author(self):
        return self.get(fields.USERNAME_AUTHOR, self[fields.USERNAME])

    @property
    def text(self):
        if not self._text:
            self._text = TweetText(self[fields.TEXT])
        return self._text

    @property
    def original_text(self):
        return self[fields.TEXT]

    def is_retweet(self):
        return fields.RETWEET_COUNT in self

    @property
    def hashtags(self):
        if not self._hashtags:
            self._hashtags = self.hashtags_pattern.findall(
                self[fields.TEXT].lower())
        return self._hashtags

    def translate(self, lang, translate_hashtags=True):
        if self[fields.LANG] == lang:
            return

        # remove emoji characters because googletrans can't handle them
        text = self.non_bmp_pattern.sub('', self[fields.TEXT])
        # threat hashtags like normal words if required
        if translate_hashtags:
            text = text.replace('#', '')
        # unknown language will be automatically indentified
        src_lang = (self[fields.LANG]
                    if self[fields.LANG] != UNKNOWN_LANG else AUTO_LANG)
        self._text = TweetText(self.translator.translate(text,
                                                         src=src_lang,
                                                         dest=lang).text)
