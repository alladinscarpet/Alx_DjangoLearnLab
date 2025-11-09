'''URL routing'''

from django.urls import path
from . import views
from .views import LibraryDetailView

#  e.g. when someone visits the root of this app (/polls/),
# r
urlpatterns = [
    # ex: /polls/
    path("",views.index, name="index"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

]
