from django import forms

from .models import NewsLetter

class NewsLetterSignUpForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('email',)