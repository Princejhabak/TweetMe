from django.shortcuts import render, redirect
from .models import Profile
from django.urls import reverse, reverse_lazy
from . import forms
from django.views.generic import CreateView


class Signup(CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


def follow(request, pk):
    object = Profile.objects.get(user=pk)

    object.save()
    object.followers.add(request.user)

    return redirect('tweet:detail', pk=pk)


def unfollow(request, pk):
    object = Profile.objects.get(user=pk)

    object.followers.remove(request.user)
    object.save()
    return redirect('tweet:detail', pk=pk)



