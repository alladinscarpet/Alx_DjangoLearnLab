"""
Takes Notification objects
Converts them into JSON-safe data
Controls what fields are exposed
"""

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'actor',
            'verb',
            'is_read',
            'timestamp'
        ]
