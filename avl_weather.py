#!/usr/bin/env python

from random import choice
from urllib2 import HTTPError

import tweepy

from lib.objects import RedisConnector
from lib.objects import NoDataInRedis

from private import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

class Main(object):
    def __init__(self, ):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        self.update()

    def update(self):
        r = RedisConnector()
        temp = r.get('avl_weather:current:temp')
        cond = r.get('avl_weather:current:cond')
        today_high = r.get('avl_weather:today:high')
        today_low = r.get('avl_weather:today:low')
        tom_high = r.get('avl_weather:tomorrow:high')
        tom_low = r.get('avl_weather:tomorrow:low')
        if (temp and cond and tom_high and tom_low):
            tweet = "It's %sF and %s in %s. Today's high %sF, low: %sF Tomorrow's high %sF, low: %sF #boone #wncwx"
            name = choice('ashevegas,ashetana,ashetopia'.split(','))
            self.tweet = tweet % (temp, cond, name, today_high, today_low, tom_high, tom_low)
            try:
                self.api.update_status(self.tweet)
            except HTTPError:
                # fail whale ftw
                pass
            except tweepy.error.TweepError:
                # duplicate tweet.
                pass
        else:
            raise NoDataInRedis


if __name__ == '__main__':
    Main()

