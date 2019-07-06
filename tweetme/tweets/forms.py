from django import forms

from .models import Tweet, TweetReply


class TweetModelForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(
                                  attrs={'placeholder': "Your message",
                                         "class": "form-control"}
                              ))

    class Meta:
        model = Tweet
        fields = [
            "content"
        ]

    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        if content == "abc":
            raise forms.ValidationError("Cannot be ABC")
        return content


class TweetReplyModelForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(
                                  attrs={'placeholder': "Your reply",
                                         "class": "form-control"}
                              ))

    class Meta:
        model = TweetReply
        fields = [
            "content"
        ]
