'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from rest_framework import filters

from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator




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







#----------------------------------------posts feed views------------------------------------------------------#

class FeedView(generics.GenericAPIView):
    """
    Endpoint to fetch posts from users the current user is following.
    Posts are returned in descending order of creation date (most recent first).
    Supports pagination with ?page=<number>.
    """
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access feed

    def get(self, request):
        # Get the currently logged-in user
        current_user = request.user

        # Get users this user is following
        following_users = current_user.following.all()

        # Fetch posts by followed users, newest first
        posts_queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Pagination: 10 posts per page
        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts_queryset, 10)
        page_obj = paginator.get_page(page_number)

        # Serialize the posts for API response
        serializer = PostSerializer(page_obj, many=True)

        # Return serialized data with pagination info
        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "results": serializer.data
        }, status=status.HTTP_200_OK)



#-------------------------------------likes------------------------------------------------#
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Like
from notifications.models import Notification


class LikePostView(APIView):
    """Allows authenticated users to like a post"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Fetch the post
        post = get_object_or_404(Post, pk=pk)

        # Prevent duplicate likes
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create notification for post author
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

        return Response(
            {"detail": "Post liked."},
            status=status.HTTP_201_CREATED
        )


class UnlikePostView(APIView):
    """Allows users to remove their like"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if not like:
            return Response(
                {"detail": "You haven't liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        like.delete()
        return Response(
            {"detail": "Post unliked."},
            status=status.HTTP_200_OK
        )

