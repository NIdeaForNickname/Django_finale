from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Category, Post, Comment
from .forms import (UserRegistrationForm, UserLoginForm, UserUpdateForm, 
                    CategoryForm, PostForm, CommentForm)

def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'categories': categories})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'forum/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=nickname, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {nickname}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid nickname or password.')
    else:
        form = UserLoginForm()
    return render(request, 'forum/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def user_profile(request, nickname):
    user = get_object_or_404(User, nickname=nickname)
    return render(request, 'forum/profile.html', {'profile_user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
            return redirect('user_profile', nickname=request.user.nickname)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'forum/edit_profile.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = User.objects.get(pk=request.user.pk)
            category.save()
            messages.success(request, 'Success!')
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'forum/create_category.html', {'form': form})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.category = category
            post.author = User.objects.get(pk=request.user.pk)
            post.save()
            messages.success(request, 'Success!')
            return redirect('category_detail', pk=pk)
    else:
        form = PostForm() if request.user.is_authenticated else None
    
    return render(request, 'forum/category_detail.html', {
        'category': category,
        'posts': posts,
        'form': form
    })

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.user == category.created_by:
        category.delete()
        messages.success(request, 'Success!')
    else:
        messages.error(request, 'You can only delete your own categories.')
    return redirect('home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = User.objects.get(pk=request.user.pk)
            comment.save()
            messages.success(request, 'Success!')
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm() if request.user.is_authenticated else None
    
    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category_pk = post.category.pk
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Success!')
    else:
        messages.error(request, 'You can only delete your own posts.')
    return redirect('category_detail', pk=category_pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
        messages.success(request, 'Success!')
    else:
        messages.error(request, 'You can only delete your own comments.')
    return redirect('post_detail', pk=post_pk)

@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
    return redirect('post_detail', pk=pk)

@login_required
def toggle_comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': comment.total_likes()})
    return redirect('post_detail', pk=comment.post.pk)