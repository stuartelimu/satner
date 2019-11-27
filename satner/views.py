from django.views.generic.base import TemplateView
from .forms import ContactForm
from django.views.generic.edit import FormView
from marketing.forms import NewsLetterSignUpForm

class AboutPageView(TemplateView):

    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsLetterSignUpForm()
        return context


class ServicesPageView(TemplateView):

    template_name = "services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsLetterSignUpForm()
        return context


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
