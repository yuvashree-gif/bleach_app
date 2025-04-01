from django.urls import path
from .views import post_list, post_create, react_to_post, login_view, home_view, register_view  # Import the home view


urlpatterns = [
    path('', home_view, name='home'),  # Home page
    path('posts/', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('login/', login_view, name='login'),  # Change to point to login_view instead of register_view
    path('register/', register_view, name='register'),  # Add registration view

    path('react/<int:post_id>/', react_to_post, name='react_to_post'),
]
