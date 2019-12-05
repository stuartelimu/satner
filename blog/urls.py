from django.urls import path
from django.views.decorators.http import require_POST
from .views import PostDetailView, PostListView, CategoryListView, search

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('category/<category_slug>/', CategoryListView.as_view(), name='category-post-list'),
    path('search/results/', search, name='search'),
]