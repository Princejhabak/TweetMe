from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('tweets.urls', namespace="tweet")),
    url(r'accounts/', include('accounts.urls', namespace="accounts")),
    url(r'accounts/', include('django.contrib.auth.urls')),
]
