from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import *


def index(request):
    # Get all posts
    posts = Post.objects.all()
    return render(request, "network/index.html",{
        'posts': posts
    })

def profile_view(request,user):
    print(user)
    # Get user object
    user_obj = User.objects.get(username=user)
    print(user_obj)
    # Get user profile
    profile = Profile.objects.get(user=user_obj)
    print(profile)
    # Get all user's posts
    posts = Post.objects.filter(user=user)
    print(posts)
    return render(request,'network/profile.html',{'profile':profile})

# Create post
def create_post(request):
    if request.method == 'POST':
        user = request.user.username
        content = request.POST['content']
        new_post = Post.objects.create(user=user,content=content)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create user profile for user
            new_profile = Profile.objects.create(id_user=user.id,user=user)
            new_profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
