from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.encoding import python_2_unicode_compatible

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    slug = models.SlugField(max_length=120, unique_for_date='created_on')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


