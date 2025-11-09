'''URL routing'''

from django.urls import path
from .views import list_books, LibraryDetailView


#  e.g. when someone visits the root of this app (/rship/),
#
urlpatterns = [
    # ex: /polls/
    path("",list_books, name="index"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),

]
