from django.db import models
from tweets.models import Tweet
from django.conf import settings
from django.contrib.auth.models import User, PermissionsMixin


class User(User, PermissionsMixin):

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)


    def __str__(self):
        return self.user.username