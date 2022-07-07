
from django.urls import path

from ServerApi import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<user_id>/', views.user),
    path('login/', views.login),

    path('posts/', views.post_list),
    path('posts/<int:post_id>/', views.post_edit),
    path('posts/<int:post_id>/comments/', views.post_comments)
]
