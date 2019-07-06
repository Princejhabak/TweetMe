from django.db import models
from django.conf import settings
from django.urls import reverse


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    retweeted = models.BooleanField(default=False)
    retweetd_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='retweet_by')

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-timestamp']


class TweetReply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class TweetLike(models.Model):
    liked_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
    # likes = models.IntegerField(default=0)
