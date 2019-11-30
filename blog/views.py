from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from hitcount.views import HitCountDetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from .models import Post, Category, Comment
from .forms import CommentForm
from marketing.forms import NewsLetterSignUpForm

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created_on')
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:4]
        context['categories'] = Category.objects.all()
        context['form'] = NewsLetterSignUpForm()
        return context


class PostDetailView(FormMixin, HitCountDetailView):
    form_class = CommentForm
    model = Post
    context_object_name = 'post'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(active=True, post=self.object)
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:4]
        context['categories'] = Category.objects.all()
        context['form'] = NewsLetterSignUpForm()
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        # attach current post to the comment
        self.object = self.get_object()
        
        form = self.get_form() # create instance of form class
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        
        return super().form_valid(form)


class CategoryListView(ListView):
    context_object_name = 'posts'
    template_name = 'category_post_list.html'
    def get_queryset(self):
        queryset = Post.objects.filter(
            categories__name__contains=self.kwargs['category_slug']
        ).order_by('-created_on')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:4]
        context['form'] = NewsLetterSignUpForm()
        return context
    
    




