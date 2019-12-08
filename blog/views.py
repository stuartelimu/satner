from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from hitcount.views import HitCountDetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from .models import Post, Category, Comment
from .forms import CommentForm
from marketing.forms import NewsLetterSignUpForm

import bs4
import requests

WPM = 200
WORD_LENGTH = 5

def extract_text(url):
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    return texts

def is_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == "\n":
        return False
    return True

def filter_visible_text(page_texts):
    return filter(is_visible, page_texts)

def count_words_in_text(text_list, word_length):
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text)/word_length
    return total_words

def estimate_reading_time(url):
    texts = extract_text(url)
    filtered_text = filter_visible_text(texts)
    total_words = count_words_in_text(filtered_text, WORD_LENGTH)
    return total_words/WPM

# print(estimate_reading_time('http://127.0.0.1:8000/blog/test/'))
# article_reading_time = request.session.get(post.slug)

def get_article_reading_time():
    object_list = Post.objects.all().order_by('-created_on')
    for obj in object_list:
        post_url = "http://127.0.0.1:8000/blog/test/"
        print("ellp")
        reading_time = round(estimate_reading_time(post_url))
        return({obj.pk: reading_time})

# print(get_article_reading_time())

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }

    return render(request, 'blog/search_results.html', context=context)



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created_on')
    paginate_by = 6
    

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        reading_times = {}
        for obj in self.get_queryset():
            post_url = self.request.build_absolute_uri(obj.get_absolute_url())
            reading_times[obj.slug] = estimate_reading_time(post_url)
            self.request.session[obj.slug] = estimate_reading_time(post_url)

        print(reading_times)
        # context['reading_times'] = reading_times
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
        context['reading_time'] = estimate_reading_time(self.request.build_absolute_uri(self.object.get_absolute_url()))
        context['comments'] = Comment.objects.filter(active=True, post=self.object)
        # context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:4]
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



    
    




