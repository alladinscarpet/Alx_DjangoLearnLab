from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# Create router
# Router automatically generates all the necessary URLs for each
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# Define URL patterns
urlpatterns = [
    # router handles all CRUD URLs
    # GET /api/posts/ → list posts
    # POST /api/posts/ → create post
    # GET /api/posts/<id>/ → retrieve post
    # PUT /api/posts/<id>/ → update post
    # DELETE /api/posts/<id>/ → delete post
    path('', include(router.urls)),

    # ex: GET /api/feed/
    path('feed/', FeedView.as_view(), name='feed'),
]
