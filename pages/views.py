from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from pages.models import PostModel


def index_view(request):
    users = User.objects.prefetch_related("authormodel").all()
    posts = PostModel.objects.select_related("author", "author__user").all()

    context = {
        'users': users,
        'posts': posts
    }
    return render(request, "index.html", context)


def user_posts_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    users = User.objects.prefetch_related("authormodel").all()
    posts = PostModel.objects.filter(author__user=user_profile).select_related("author", "author__user")

    context = {
        'users': users,
        'posts': posts,
        'selected_user': user_profile
    }
    return render(request, "index.html", context)

from django.contrib.auth.decorators import login_required

@login_required
def my_posts_view(request):
    users = User.objects.prefetch_related("authormodel").all()
    posts = PostModel.objects.filter(author__user=request.user).select_related("author", "author__user")

    context = {
        'users': users,
        'posts': posts,
        'selected_user': request.user   # faqat login bo‘lgan user
    }
    return render(request, "index.html", context)
