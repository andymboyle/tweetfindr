from __future__ import unicode_literals

from django.db import models


class TwitterAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    twitter_id = models.BigIntegerField(unique=True)
    oauth_token = models.CharField(max_length=60)
    oauth_secret = models.CharField(max_length=60)

    class Meta:
        db_table = 'twitter_accounts'
