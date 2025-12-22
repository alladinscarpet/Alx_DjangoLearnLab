from django.urls import path, include
from .views import NotificationListView



# Define URL patterns
urlpatterns = [
    # ex: GET /api/notifications/
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]
