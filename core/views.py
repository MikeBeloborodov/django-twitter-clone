from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . import models, forms

def home_page(request):
    if request.user.is_authenticated:
        return redirect('twitter_feed')
    else:
        return redirect('login_user')

def register_user(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')
        else:
            messages.error(request, 'Registration error')
            return redirect('register_user')
    form = forms.RegisterUserForm()
    context = {
        'form': form,
    }
    return render(request, 'core/register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('twitter_feed')
        else:
            messages.error(request, 'Login error, check your credentials and try again.')
            return redirect('login_user')
    context = {}
    return render(request, 'core/login.html', context)

@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        body = request.POST.get('body')    
        models.Tweet.objects.create(
            user = user,
            body = body,
        )
        return redirect(f'/user/{user.id}')
    tweets = models.Tweet.objects.filter(
        Q(user=user) |
        Q(retweets=user) 
        ).order_by('-created')
    context = {
        'user': user,
        'tweets': tweets,
    }
    return render(request, 'core/user_profile.html', context)

@login_required(login_url='login_user')
def twitter_feed(request):
    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ""
    tweets = models.Tweet.objects.filter(body__icontains=q).order_by('-created')
    context = {
        'tweets': tweets,
    }
    return render(request, 'core/twitter_feed.html', context)

@login_required(login_url='login_user')
def like_tweet(request, pk):
    user = User.objects.get(username=request.user)
    tweet = models.Tweet.objects.get(id=pk)
    if tweet.likes.filter(username=user.username):
        tweet.likes.remove(user)
    else:
        tweet.likes.add(user)
    return redirect('twitter_feed')

@login_required(login_url='login_user')
def retweet(request, pk):
    user = User.objects.get(username=request.user)
    tweet = models.Tweet.objects.get(id=pk)
    if tweet.retweets.filter(username=user.username):
        tweet.retweets.remove(user)
    else:
        tweet.retweets.add(user)
    return redirect('twitter_feed')