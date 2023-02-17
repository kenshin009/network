from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *


@login_required(login_url='login')
def index(request):
    # Get all posts
    posts = Post.objects.all()
     # check how many posts this user liked
    liked_posts_all = []
    for post in posts:
        liked_posts = LikePost.objects.filter(user=request.user.username,post_id=post.id)
        liked_posts_all.extend(liked_posts)

    return render(request, "network/index.html",{
        'posts': posts,
        'liked_posts': liked_posts_all
    })

def following(request):
    # Get all follows of request user
    follows = Follow.objects.filter(user_follow=request.user)
    # Get all user_profiles that request user has followed
    users_profiles = []
    for follow in follows:
       users_profiles.append(follow.user_profile)
    # Get all posts of the user_profiles that request user has followed
    all_posts = []
    for user in users_profiles:
       posts = Post.objects.filter(user=user)
       all_posts.extend(posts)
       print(all_posts)
    
    # check how many posts this user liked
    liked_posts_all = []
    for post in all_posts:
        liked_posts = LikePost.objects.filter(user=request.user.username,post_id=post.id)
        liked_posts_all.extend(liked_posts)

    return render(request,'network/following.html',{
        'posts': all_posts,
        'user_request': request.user.username,
        'liked_posts': liked_posts_all
    })

@csrf_exempt
def follows(request):

    if request.method == 'POST':
        # Get new follow
        data = json.loads(request.body)
        # Create new follow
        new_follow = Follow.objects.create(user_follow=data['user_follow'],user_profile=data['user_profile'])
        new_follow.save()
        # # Get both users and users' profiles
        user_follow = User.objects.get(username=data['user_follow'])
        user_profile = User.objects.get(username=data['user_profile'])
        user_follow_p = Profile.objects.get(user=user_follow)
        user_profile_p = Profile.objects.get(user=user_profile)
        # # Update followers count and following count of both users' profiles
        user_follow_p.following += 1
        user_follow_p.save()
        user_profile_p.followers += 1
        user_profile_p.save()

        # Modify data
        new_data = {
            "profile_follower": user_profile_p.followers,
            "already_followed": True
        }
    elif request.method == 'PUT':
        # Get follow json data
        data = json.loads(request.body)
        # Check whether request user has already followed or not
        follow_exist = Follow.objects.filter(user_follow=data['user_follow'],user_profile=data['user_profile']).first()
        if follow_exist is not None:
            # if already followed,delete it
            follow_exist.delete()
            # Get both users and users' profiles
            user_follow = User.objects.get(username=data['user_follow'])
            user_profile = User.objects.get(username=data['user_profile'])
            user_follow_p = Profile.objects.get(user=user_follow)
            user_profile_p = Profile.objects.get(user=user_profile)
            # # Update followers count and following count of both users' profiles
            user_follow_p.following -= 1
            user_follow_p.save()
            user_profile_p.followers -= 1
            user_profile_p.save()

            # Modify data
            new_data = {
                "profile_follower": user_profile_p.followers,
                "already_followed": False
            }
            print('already followed')
        else:
            # if not already followed, create new follow
            new_follow = Follow.objects.create(user_follow=data['user_follow'],user_profile=data['user_profile'])
            new_follow.save()
            # # Get both users and users' profiles
            user_follow = User.objects.get(username=data['user_follow'])
            user_profile = User.objects.get(username=data['user_profile'])
            user_follow_p = Profile.objects.get(user=user_follow)
            user_profile_p = Profile.objects.get(user=user_profile)
            # # Update followers count and following count of both users' profiles
            user_follow_p.following += 1
            user_follow_p.save()
            user_profile_p.followers += 1
            user_profile_p.save()

            # Modify data
            new_data = {
                "profile_follower": user_profile_p.followers,
                "already_followed": True
            }
            print('Not followed yet')
            return JsonResponse(new_data,status=200)

        return JsonResponse(new_data,status=200)
    else:
        return JsonResponse({"Error":"Post request required"},status=404)

    return JsonResponse(new_data,status=200)

@csrf_exempt
def like_posts(request):
    
    if request.method == "POST":
        # Get new like
        data = json.loads(request.body)
        # Create new like
        new_like = LikePost.objects.create(post_id=data['post_id'],user=data['user'])
        new_like.save()
        # Modify data
        data = {
            "id": new_like.id,
            "post_id": new_like.post_id,
            "liked_by": new_like.user
        }

    elif request.method == "GET":
        likes = LikePost.objects.all()
        all_likes = [{"id":like.id,"post_id":like.post_id,"user":like.user} for like in likes]
        data = {
            "response": all_likes
        }
    else:
        return JsonResponse({"Error":"Get or Post request required"},status=404)
    return JsonResponse(data,status=200)

@csrf_exempt
def like_post_detail(request,post_id):  

    if request.method == "PUT":
        # Get the liked post
        liked_post = Post.objects.get(id=post_id)
        data = json.loads(request.body)

        # Check the user has already liked the post or not
        like_filter = LikePost.objects.filter(post_id=data['post_id'],user=data['user']).first()
        if like_filter is not None:
            # if already liked by user, delete like and decrement like count
            like_filter.delete()
            liked_post.likes -= 1
            liked_post.save()
            # Modify the data
            data = {
                "id": liked_post.id,
                "user": liked_post.user,
                "liked_by": '',
                "likes": liked_post.likes
            }
            
        else:
            # if not already liked by user, create new like and increment like count
            new_like = LikePost.objects.create(post_id=data['post_id'],user=data['user'])
            new_like.save()
            liked_post.likes += 1
            liked_post.save()
            # Modify the data
            data = {
                "id": liked_post.id,
                "user": liked_post.user,
                "liked_by": new_like.user,
                "likes": liked_post.likes
            }
            return JsonResponse(data,status=200)

        return JsonResponse(data,status=200)

    elif request.method == "GET":
        
         # Filter all likes of the specific post
        likes = LikePost.objects.filter(post_id=post_id)
        likes_in_post = [{"id":like.id,"post_id":like.post_id,"user":like.user} for like in likes]
        data = {
            "response": likes_in_post
        }
        return JsonResponse(data,status=200)
    else:
        # it must be Get or Put request
        return JsonResponse({"Error":"GET or PUT request required"},status=404)

    


@login_required(login_url='login')
def profile_view(request,user):
  
    # Get user_profile
    user_profile = User.objects.get(username=user)
    # Get profile of user_profile
    profile = Profile.objects.get(user=user_profile)
    # Get all user_profile's posts
    posts = Post.objects.filter(user=user)
    # Check request user has already followed this user profile
    already_followed = Follow.objects.filter(user_follow=request.user.username,user_profile=user_profile.username).first()

    liked_posts_all = []
    for post in posts:
        liked_posts = LikePost.objects.filter(user=request.user.username,post_id=post.id)
        liked_posts_all.extend(liked_posts)

    return render(request,'network/profile.html',{
        'profile':profile,
        'posts':posts,
        'user_profile': user_profile.username,
        'user_request': request.user.username,
        'already_followed': already_followed,
        'liked_posts': liked_posts_all
    })

@login_required(login_url='login')
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

def posts_list(request):

    # Get all the posts
    posts = Post.objects.all()
    posts_list = [{"id":post.id,"user":post.user,"content":post.content,"created_at":post.created_at,"likes":post.likes} for post in posts]
    data = {
        "response": posts_list,
    }
    return JsonResponse(data)

@csrf_exempt
def post_detail(request,post_id):

    if request.method != 'PUT':
        return JsonResponse({"Error":"PUT request required"},status=400)

    data = json.loads(request.body)
    status = 200
    # Get specific post detail
    try:
        # Increment post likes by 1
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        # Add changed data 
        data['user'] = post.user
        data['content'] = post.content
        data['created_at'] = post.created_at
        data['likes'] = post.likes
    except:
        data['message'] = 'Not Found'
        status = 404

    return JsonResponse(data,status=status)

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
