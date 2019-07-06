from django.contrib import admin
from .models import Tweet, TweetReply, TweetLike

# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweetReply)
admin.site.register(TweetLike)