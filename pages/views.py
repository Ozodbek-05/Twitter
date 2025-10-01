from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


@login_required
def my_posts_view(request):
    users = User.objects.prefetch_related("authormodel").all()
    posts = PostModel.objects.filter(author__user=request.user).select_related("author", "author__user")

    context = {
        'users': users,
        'posts': posts,
        'selected_user': request.user
    }
    return render(request, "index.html", context)


@login_required
def create_post_view(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if message:
            PostModel.objects.create(
                author=request.user.authormodel,
                message=message
            )
            messages.success(request, 'Post successfully created!')
        else:
            messages.error(request, 'Post message cannot be empty!')

    return redirect('pages:home')


@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(PostModel, pk=pk)

    if request.user != post.author.user:
        messages.error(request, 'You are not the owner of this post!')
        return redirect('pages:home')

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if message:
            post.message = message
            post.save()
            messages.success(request, 'Post successfully updated!')
        else:
            messages.error(request, 'Post message cannot be empty!')

    return redirect('pages:home')


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(PostModel, pk=pk)

    if request.user != post.author.user:
        messages.error(request, 'You are not the owner of this post!')
        return redirect('pages:home')

    post.delete()
    messages.success(request, 'Post successfully deleted!')

    return redirect('pages:home')