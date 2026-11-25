from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PostForm, ProfilePictureForm
from .models import PageProfile, Post

def dashboard(request):
    profile, _ = PageProfile.objects.get_or_create(pk=1)
    profile_picture_form = ProfilePictureForm(instance=profile)

    if request.method == 'POST' and request.POST.get('action') == 'delete_profile_picture':
        if profile.image:
            profile.image.delete(save=True)
            messages.success(request, 'Profile picture deleted successfully!')
        else:
            messages.info(request, 'There is no profile picture to delete.')
        return redirect('dashboard')
    elif request.method == 'POST' and request.POST.get('action') == 'profile_picture':
        profile_picture_form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        form = PostForm()
        if profile_picture_form.is_valid():
            profile_picture_form.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('dashboard')
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('dashboard')
    else:
        form = PostForm()

    posts = Post.objects.all()
    return render(request, 'accounts/dashboard.html', {
        'form': form,
        'profile': profile,
        'profile_picture_form': profile_picture_form,
        'posts': posts,
    })


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'accounts/edit_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')

    return render(request, 'accounts/delete_post.html', {'post': post})