'''URL routing'''
from django.urls import path

# login/out
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # for register

#  e.g. when someone visits the root of this app (/blog/),
urlpatterns = [
    # home page
    # ex: /blog/
    path("",views.index, name="index"),

    # Auth routes
    # ex: /blog/login
    path('login/',  LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile_view, name="profile"),

    # CRUD routes
    # ex: GET /blog/posts
    path('posts/', views.PostListView.as_view(), name='post-list'),

    # ex: GET blog/posts/<pk>/
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # ex: POST blog/post/new/
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),

    # ex: PUT/PATCH blog/post/<pk>/update/
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),

    # ex: DELETE blog/posts/<pk>/delete/
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),


    # Comments
    # ex: POST blog/poss/1/comments/new/
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),

    # ex: PUT/PATCH blog/comments/<pk>/edit/
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-edit"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),


    # Tags
    path('search/', views.search, name='search'),
    # View posts by tag
    path('tags/<str:tag_name>/', views.TaggedPostListView.as_view(), name='tagged-posts'),
]