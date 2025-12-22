'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from rest_framework import filters


# Custom permission to allow editing only by author
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Checks whether the current user is the author of a post or comment.
    Allows anyone to read (GET) but only the author can modify (PUT/PATCH/DELETE).
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only allowed to author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """Provides all CRUD operations for posts automatically."""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    #  # Set the logged-in user as the author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Enable filtering, searching
    filter_backends = [filters.SearchFilter]


class CommentViewSet(viewsets.ModelViewSet):
    """Handles all CRUD operations for comments."""
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Automatically assigns the logged-in user as the author of the comment.
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

