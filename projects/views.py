from django.views.generic import ListView, DetailView

from .models import Project

from marketing.forms import NewsLetterSignUpForm

class ProjectListView(ListView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['form'] = NewsLetterSignUpForm()
        return context


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['form'] = NewsLetterSignUpForm()
        return context