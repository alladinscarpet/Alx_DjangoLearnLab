'''User input to models'''


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment
from taggit.forms import TagWidget


# Use the project's current User model, whether it's the default Django User or a custom one
User = get_user_model()

# extend Django's built-in UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# handles editing existing user information (username + email).
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


# ModelForm for create/edit posts
class PostForm(forms.ModelForm):
    '''
    Form for creating and editing blog posts.
    Uses django-taggit's TagWidget for tag input.
    We exclude author and published_date from the form; author will be set in the view.'''
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 10}),
            'tags': TagWidget(),  # Use checkbox select for multiple tags
        }


class CommentForm(forms.ModelForm):
    """
    Automatically creates a textarea for writing a comment
    Ensures the comment matches the Comment model rules
    Handles:
    validation (e.g. empty comments)
    cleaning user input
    saving the comment to the database
    """
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your comment here..."
            })
        }

