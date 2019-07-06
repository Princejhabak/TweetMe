from django.conf.urls import url
from . import views

app_name = 'tweets'

urlpatterns = [
    url(r'^$', views.tweet_list_view, name='list'),
    url(r'^delete/(?P<pk>\d+)/$', views.TweetDeleteView.as_view(), name='delete'),
    url(r'^user/(?P<pk>\d+)/$', views.user_detail_view, name='detail'),
    url(r'^reply/(?P<pk>\d+)/$', views.tweet_reply_view, name='reply'),
    url(r'^retweet/(?P<pk>\d+)/$', views.tweet_retweet_view, name='retweet'),
    url(r'^like/(?P<pk>\d+)/$', views.tweet_like_view, name='like'),
]