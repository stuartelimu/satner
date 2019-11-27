from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

import json
import requests

from .forms import NewsLetterSignUpForm
from .models import NewsLetter

def subscribe(email):

    API_KEY = settings.SEND_GRID_API_KEY
    LIST_ID = settings.SEND_GRID_LIST_ID

    url = "https://api.sendgrid.com/v3/marketing/contacts"

    payload = {"list_ids": [LIST_ID], "contacts": [{"email": email}]}
    headers = {'authorization': f'Bearer {API_KEY}'}

    response = requests.request("PUT", url, data=payload, headers=headers)

    return response.status_code

def email_list_signup(request):
    form = NewsLetterSignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email_signup_qs = NewsLetter.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.error(request, "You are already subscribed")
            else:
                subscribe(form.instance.email)
                form.save()
                messages.info(request, "Thank you for subscribing to our newsletter")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
