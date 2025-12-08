from django.contrib import admin

from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('author', 'title', 'content', 'published_date')
