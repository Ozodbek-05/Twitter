from django.urls import path
from pages.views import index_view, user_posts_view, my_posts_view

app_name = 'pages'

urlpatterns = [
    path('', index_view, name='home'),
    path('user/<str:username>/', user_posts_view, name='user_posts'),
    path('my-posts/', my_posts_view, name='my_posts'),
]
