from django.contrib import admin
from .models import Book

# custom usr
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


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


# Extending Django’s built-in UserAdmin with a custom one
class CustomUserAdmin(UserAdmin):
    # When dealing with users in admin, use my custom user model.
    model = CustomUser

    # controls the columns in the admin display table.
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
    )

    # fields in admin panel (add/edit)
    # controls what you see when editing an existing user
    # Take all the default fields Django shows and
    # append a new section called Additional Info that includes my extra fields.
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # When an admin clicks “Add User”,
    # they also see the two new fields so as to set them when creating a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            'classes': ('wide',),
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
# Use the CustomUserAdmin rules when displaying my CustomUser model in the admin.
admin.site.register(CustomUser, CustomUserAdmin)