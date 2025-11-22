'''
A serializer converts:
Python/Django model instances → JSON (for API responses)
JSON → Python data (for POST/PUT requests later)
Think of a serializer as Pydantic for Django.
'''

from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
