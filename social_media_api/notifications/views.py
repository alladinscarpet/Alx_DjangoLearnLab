from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """Returns logged-in user’s notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only notifications for the logged-in user
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-timestamp')

