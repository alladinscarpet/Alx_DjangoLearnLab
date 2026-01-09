from django.urls import path
from .views import (
    PostListCreateView, 
    PostDetailView, 
    LikePostView, 
    UnlikePostView
)

# Define URL patterns
urlpatterns = [
    # List all posts or create a new post
    # GET /api/posts/ → list posts
    # POST /api/posts/ → create post
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    
    # Retrieve, update, or delete a specific post
    # GET /api/posts/<id>/ → retrieve post
    # PUT /api/posts/<id>/ → update post
    # DELETE /api/posts/<id>/ → delete post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Like/Unlike posts
    # POST /api/posts/<id>/like/
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    # POST /api/posts/<id>/unlike/
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
