from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField(max_length=120)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        send_mail(self.cleaned_data['subject'], self.cleaned_data['message'], self.cleaned_data['email'], ['stuartelimu@gmail.com'], fail_silently=False)