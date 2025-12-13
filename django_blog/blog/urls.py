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
    # ex: POST blog/posts/create/
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    # ex: PUT/PATCH blog/posts/update/<pk>
    path('blog/posts/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    # ex: DELETE blog/posts/delete/<pk>
    path('posts/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
]