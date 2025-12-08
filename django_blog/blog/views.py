'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView

# login/out
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post


# Create your views here.
def index(request):
    """
    Landing page view for the blog.
    Displays a welcome message and the latest 5 blog posts.
    """
    latest_posts = Post.objects.order_by('-published_date')[:5]  # latest 5 posts
    context = {
        "latest_posts": latest_posts,
        "welcome_message": "Welcome to My Django Blog!"
    }
    return render(request, "blog/index.html", context)

def register(request):
    """
    register view
    GET  -> show empty registration form
    POST -> validate and create user, then log them in
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)                # log in immediately
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("index")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile_view(request):
    """
    Handles viewing and updating user profile
    GET → Shows the form pre-filled with the user’s current info.
    POST → Updates the user profile if the form is valid.
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})
