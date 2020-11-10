from backend.posts.models import Post
from django.urls import path
from .views import ListPosts, show_user_ip, PostsViewSet


app_name = 'posts'

urlpatterns = []
 
# API URLs
urlpatterns += [
    # path("", ListPosts.as_view(), name="posts"),
    # path("posts", show_user_ip, name="posts"),
]