from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    @staticmethod
    def store_tokens(user, access_token, refresh_token, token_expiry):
        expiration_time = datetime.now() + timedelta(seconds=token_expiry)

        token, created = SpotifyToken.objects.get_or_create(user=user)
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_at = expiration_time
        token.save()

