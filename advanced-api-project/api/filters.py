'''
Instead of manually writing filtering logic,
we use a FilterSet to tell DRF:
“These are the fields and comparisons users can filter with.”
'''

import django_filters
from .models import Book

# The FilterSet tells DRF which fields users can filter on and what types of lookups are allowed.
class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author__name': ['icontains'],   # nested filtering
        }
