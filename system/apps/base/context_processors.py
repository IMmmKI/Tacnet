from django.conf import settings
import tweetpony
from django.core.cache import *


def Twitter(request):

    tweets = cache.get('tweets')

    if not tweets:

        try:
            api = tweetpony.API(consumer_key=settings.TWITTER_OAUTH['consumer_key'],
                                consumer_secret=settings.TWITTER_OAUTH['consumer_secret'],
                                access_token=settings.TWITTER_OAUTH['access_token'],
                                access_token_secret=settings.TWITTER_OAUTH['access_token_secret'])

            tweetRequest = api.user_timeline(count=1)
            if tweetRequest:
                tweets = tweetRequest
                cache.set('tweets', list(tweets), timeout=3600)

        except tweetpony.APIError:
            tweets = None

    if tweets:
        tweet = tweets[0]
    else:
        tweet = None

    return {'twitter_tweet': tweet, 'twitter_link': "https://twitter.com/" + settings.TWITTER_OAUTH['user'], 'twitter_user':settings.TWITTER_OAUTH['user']}
