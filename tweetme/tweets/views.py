from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.core.paginator import Paginator

from .models import Tweet, TweetReply, TweetLike
from .forms import TweetModelForm, TweetReplyModelForm
from accounts.models import Profile


@login_required
def tweet_list_view(request):
    queryset = Tweet.objects.all()
    users_queryset = Profile.objects.all()

    paginator = Paginator(queryset, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    tweets = paginator.get_page(page)

    if request.method == "POST":

        answer_form = TweetModelForm(request.POST)

        if answer_form.is_valid():
            answer = answer_form.save(commit=False)

            answer.user = request.user
            answer.content = answer_form.cleaned_data['content']
            answer.retweetd_by = request.user
            answer.save()

            return redirect('tweet:list')
    else:
        answer_form = TweetModelForm()

    query = request.GET.get("q", None)
    if query is not None:
        qs_tweet = queryset.filter(Q(content__icontains=query) | Q(user__username__icontains=query) | Q(
            retweetd_by__username__icontains=query))
        qs_user = users_queryset.filter(Q(user__username__icontains=query))

        mylist = []
        for object in qs_user:
            mylist.append(object.user)
        mylist = list(dict.fromkeys(mylist))

        return render(request, 'tweets/search.html', {'tweets': qs_tweet, 'users': mylist})
    else:
        return render(request, 'tweets/tweet_list.html', {'tweets': tweets, 'form': answer_form})


@login_required
def user_detail_view(request, pk):
    queryset = Tweet.objects.filter(retweetd_by=pk)

    # followers = Profile.objects.get(user=queryset.first().user)
    if queryset:
        followers = queryset.first().retweetd_by.profile_set.first()
        following = Profile.objects.filter(followers=queryset.first().retweetd_by)

        l = []
        for x in followers.followers.all():
            l.append(x)

        return render(request, 'tweets/user_detail.html',
                      {'tweets': queryset, 'followers': followers, 'following': following, 'followers_list': l, 'xuser':followers.user})

    else:
        followers = Profile.objects.get(user=pk)
        following = Profile.objects.filter(followers=pk)
        l = []
        for x in followers.followers.all():
            l.append(x)
        return render(request, 'tweets/user_detail.html',
                      {'tweets': queryset, 'followers': followers, 'following': following, 'followers_list': l, 'xuser':followers.user})


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("tweet:list")


@login_required
def tweet_reply_view(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    # x = tweet.tweetlike_set.get(liked_tweet=tweet)
    # print(x.liked_by.count())
    replies = TweetReply.objects.filter(tweet=tweet)

    if request.method == "POST":
        answer_form = TweetReplyModelForm(request.POST)

        if answer_form.is_valid():
            answer = answer_form.save(commit=False)

            answer.tweet = tweet
            answer.user = request.user
            answer.content = answer_form.cleaned_data['content']
            answer.save()

            return redirect('tweets:reply', pk=pk)
    else:
        answer_form = TweetReplyModelForm()

    query = request.GET.get("q", None)
    queryset = Tweet.objects.all()
    users_queryset = Profile.objects.all()
    if query is not None:
        qs_tweet = queryset.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
        qs_user = users_queryset.filter(Q(user__username__icontains=query))

        mylist = []
        for object in qs_user:
            mylist.append(object.user)
        mylist = list(dict.fromkeys(mylist))

        return render(request, 'tweets/search.html', {'tweets': qs_tweet, 'users': mylist})
    else:
        return render(request, 'tweets/tweet_reply.html', {'tweet': tweet, 'replies': replies, 'form': answer_form})


@login_required
def tweet_retweet_view(request, pk):
    queryset = Tweet.objects.get(pk=pk)

    answer_form = TweetModelForm()
    answer = answer_form.save(commit=False)

    answer.user = queryset.user
    answer.content = queryset.content
    answer.retweeted = True
    answer.retweetd_by = request.user
    answer.save()

    return redirect('tweet:list')
    # return render(request, 'tweets/tweet_list.html', {'tweets': queryset, 'form': answer_form})


@login_required
def tweet_like_view(request, pk):
    tweet = Tweet.objects.get(pk=pk)

    try:
        tweet_like_object = TweetLike.objects.get(liked_tweet=tweet)
        tweet_like_object.save()
        tweet_like_object.liked_by.add(request.user)

    except TweetLike.DoesNotExist:
        obj = TweetLike(liked_tweet=tweet)
        obj.save()
        obj.liked_by.add(request.user)

    return redirect('tweet:list')

