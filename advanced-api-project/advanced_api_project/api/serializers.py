'''
A serializer converts:
Python/Django model instances → JSON (for API responses)
JSON → Python data (for POST/PUT requests later)
Think of a serializer as Pydantic for Django.
'''

from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# serializes all fields of the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    # custom validation to ensure publication_year
    # is not greater than the current year.
    def validate(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model.
    Includes nested serialization of all related books using BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)
    # "books" comes from related_name='books' in the Book model.

    # Show me a list of books belonging to this object,
    # formatted using BookSerializer, but don’t allow editing these books through this serializer
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
