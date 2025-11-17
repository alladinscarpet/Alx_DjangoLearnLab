'''User input to models'''

from django.forms import ModelForm
from .models import Author, Book

class CreateAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
