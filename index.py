from twython import Twython
from twython.exceptions import TwythonError
import boto3
import json
import os


class TagKV():
    def __init__(self, arn):
        self.arn = arn
        self.client = boto3.client('lambda')

    def get(self, key, default=None):
        res = self.client.list_tags(Resource=self.arn)
        if str(key) in res['Tags']:
            return res['Tags'][str(key)]
        else:
            return default

    def set(self, key, value):
        self.client.tag_resource(
            Resource=self.arn,
            Tags={str(key): str(value)})

    def delete(self, key):
        self.client.untag_resource(
            Resource=self.arn,
            TagKeys=[str(key)])


def lc(tweet):
    original = tweet['full_text']
    out = original.lower()
    entity_indices = [e['indices']
                      for es in tweet['entities'].values() for e in es]
    for idxs in entity_indices:
        out = out[0:idxs[0]] + original[idxs[0]:idxs[1]] + out[idxs[1]:]
    out = out.replace('&lt;', '<')
    out = out.replace('&gt;', '>')
    out = out.replace('&amp;', '&')
    return out


def handler(event, context):
    env_keys = {
        'arn': 'LAMBDA_FUNCTION_ARN',
        'consumer_key': 'CONSUMER_KEY',
        'consumer_secret': 'CONSUMER_SECRET',
        'access_token': 'ACCESS_TOKEN',
        'access_token_secret': 'ACCESS_TOKEN_SECRET'
    }
    env = {}
    for k in env_keys:
        assert env_keys[k] in os.environ, env_keys[k] + ' not set'
        env[k] = os.environ[env_keys[k]]

    twitter_client = Twython(env['consumer_key'],
                             env['consumer_secret'],
                             env['access_token'],
                             env['access_token_secret'])
    kv_store = TagKV(env['arn'])
    last_seen = kv_store.get('LastSeen', 1)

    tweets = twitter_client.get_user_timeline(
        screen_name='capitalweather',
        tweet_mode='extended',
        include_rts=False,
        since_id=last_seen,
        count=200)
    out_ids = []
    for tweet in reversed(tweets):
        status = twitter_client.update_status(status=lc(tweet))
        out_ids.append(status['id'])
        kv_store.set('LastSeen', tweets[0]['id_str'])
    return out_ids
