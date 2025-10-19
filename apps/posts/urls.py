from django.urls import path

from apps.posts.views import home_view

app_name = 'posts'

urlpatterns = [
    path('',home_view)
]