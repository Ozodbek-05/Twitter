from django.urls import path
from pages import views

app_name = 'pages'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('user/<str:username>/', views.user_posts_view, name='user-posts'),
    path('my-posts/', views.my_posts_view, name='my-posts'),
    path('create-post/', views.create_post_view, name='create-post'),
    path('edit-post/<int:pk>/', views.edit_post_view, name='edit-post'),
    path('delete-post/<int:pk>/', views.delete_post_view, name='delete-post'),
]