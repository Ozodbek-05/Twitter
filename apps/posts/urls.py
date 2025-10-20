from django.urls import path
from apps.posts.views import PostView,FollowerView,CommentsView,PostUpdateDeleteView,CommentUpdateDeleteView

app_name = 'posts'
urlpatterns = [
    path('posts/', PostView.as_view()),
    path('posts/<int:pk>/', PostUpdateDeleteView.as_view()),
    path('followers/', FollowerView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('comments/<int:pk>/', CommentUpdateDeleteView.as_view()),
]
