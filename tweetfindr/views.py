from django.shortcuts import render
from django.utils import simplejson as json
from django.conf import settings
from django.http import HttpResponse as response, HttpResponseBadRequest
from tweetfindr.models import TwitterAccount
from time import strptime, strftime, mktime
import twitter
import logging


log = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html', {
        'accounts': TwitterAccount.objects.all()
    })


def find_account(request, twitter_id):
    # If it's a get request, do the logic, otherwise pass a 400
    if request.method == 'GET':
        try:
            # Check and see if this account exists
            account = TwitterAccount.objects.get(
                twitter_id=twitter_id)
            # Use the account/system creds to talk to the API
            api = twitter.Api(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                consumer_secret=settings.TWITTER_CONSUMER_SEC,
                access_token_key=account.oauth_token,
                access_token_secret=account.oauth_secret,
            )
            results = []
            statuses = api.GetHomeTimeline()
            # Create the JSON based on what was returned from the Twitter API
            # Loop through each, create and append it to results
            # NOTE: Time is created at local time (central), so subtract that
            # on the frontend, in this case 5 hours
            for status in statuses:
                tweet = {
                    "avatar_img": status.user.profile_image_url,
                    "username": status.user.screen_name,
                    "text": status.text,
                    "time_epoch_local": make_epoch_time(status.created_at),
                    "tweet_id": status.id_str,
                    "time_string": make_string_time(status.created_at),
                    "user_id": status.user.id,
                }
                results.append(tweet)
            resp = _cors_response(json.dumps(results))

            return resp
        except Exception, e:
            return HttpResponseBadRequest(
                "There was an issue with your request: %s" % e)
    else:
        return HttpResponseBadRequest("Invalid query parameter(s)")


def make_epoch_time(time_string):
    # The time is made locally, so be aware
    return mktime(strptime(time_string, "%a %b %d %H:%M:%S +0000 %Y"))


def make_string_time(time_string):
    # Returned as a string, just in case it's needed
    timestamp = strftime(
        '%Y-%m-%d %H:%M:%S',
        strptime(time_string, '%a %b %d %H:%M:%S +0000 %Y'))
    return timestamp


def _cors_response(content=None, status=200):
    resp = response()
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, OPTIONS'
    resp['Access-Control-Allow-Headers'] = 'Content-Type'
    resp['Content-Type'] = 'application/json'

    if content:
        resp.content = content

    if status:
        resp.status = status

    return resp
