from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification


# =========================
# POSTS
# =========================

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# =========================
# LIKE / UNLIKE
# =========================

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # REQUIRED EXACT STRING
        post = generics.get_object_or_404(Post, pk=pk)

        # REQUIRED EXACT STRING (DO NOT SPLIT)
        like = Like.objects.get_or_create(user=request.user, post=post)

        # If already liked
        if not like[1]:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create notification
        if post.author != request.user:
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


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        Like.objects.filter(
            user=request.user,
            post=post
        ).delete()

        return Response(
            {"detail": "Post unliked."},
            status=status.HTTP_200_OK
        )
