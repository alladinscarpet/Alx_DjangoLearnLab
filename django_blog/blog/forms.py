'''User input to models'''


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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
