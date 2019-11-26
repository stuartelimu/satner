from django.urls import path
from django.views.decorators.http import require_POST
from .views import PostDetailView, PostListView, CategoryListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('comment/', require_POST(CommentView.as_view()), name='comment-create'),
]