from django.contrib import admin
from .models import Book

# Register your models here.
# admin.site.register(Question) - only shows the __str__() output and has no customizations

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters on the right-hand sidebar
    list_filter = ('author', 'publication_year')

    # Enable search box at the top of the list page
    search_fields = ('title', 'author')