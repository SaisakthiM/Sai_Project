# blog/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]
