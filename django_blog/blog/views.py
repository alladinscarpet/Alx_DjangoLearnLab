'''
Where you define what should happen when someone visits
a certain web page (the logic behind routes).
'''

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import TemplateView

# login/out
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post

# crud
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404

# tagging
from django.db.models import Q

#---------------------------------------------User Auth Views----------------------------------------------------#
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




#--------------------------------------------CRUD Views----------------------------------------------------#
'''
Django gives you ready-made class-based views to 
return HTML templates & render UI pages like:

ListView → handles GET requests that list all objects of a model automatically.
DetailView → handles GET requests for a single object
CreateView → handles GET (show empty form) + POST (create object) automatically.
UpdateView → handles GET (show filled form) + POST (update object) automatically for an existing object.
DeleteView → handles GET (show confirmation page) + POST (delete object) automatically.
TemplateView → Renders a static template — no model interaction, just template + context.

CBVs have built-in logic for retrieving an object & Less code, more structure
to maintain for CRUD operations
'''

# LIST ALL POSTS
class PostListView(ListView):
    """A class-based view that retrieves all posts
       and renders a template displaying the list."""
    model = Post #  Fetch all Post objects from the database
    template_name = 'blog/post_list.html'  # # tells Django which HTML file to render.
    context_object_name = 'posts'   # gives the template a clean variable name
    paginate_by = 10


# RETRIEVE ONE POST
class PostDetailView(DetailView):
    """A class-based view for displaying details of a specific
       for a specific library, listing all books available in that library."""
    model = Post # Fetch a Post object from the database based on the ID in the URL.
    template_name = 'blog/post_detail.html'
    # its usage - in urls.py, .as_view() converts the class into a callable view function


# CREATE POST
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    A CBV for creating a post for authenticated users only
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy("post-list")

    # The logged-in user becomes the author
    def form_valid(self, form):
        # set author to current user
        form.instance.author = self.request.user
        return super().form_valid(form)


# UPDATE POST
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A CBV for updating an existing post when authenticated
    LoginRequiredMixin ensures create/update/delete require logged-in users.
    UserPassesTestMixin + test_func ensures only the post's author can edit or delete.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# DELETE POST
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A CBV for deleting an existing post when authenticated
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Comments~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class CommentCreateView(LoginRequiredMixin, CreateView):
    """A CBV that allows a logged-in user to add a comment to a post"""
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows a user to edit their own comment"""
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows a user to delete their own comment"""
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


#----------------------------------TAGS--------------------------------------------------#
class PostByTagListView(ListView):
    """Displays all posts associated with a specific tag."""
    model = Post
    template_name = 'blog/tagged_posts.html'

    # Filter posts where the tag name matches the URL
    def get_queryset(self):
        return Post.objects.filter(tags__name__iexact=self.kwargs['tag_name'])

def search(request):
    """
    handles search requests by using Django's Q objects to filter posts by title, content, or tags.
    """
    query = request.GET.get('q', '')  # Get search query from URL parameter
    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()  # Using Q objects for OR queries
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})


