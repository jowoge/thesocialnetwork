from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics

# Create your views here.
# class Index(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'index.html')

# I wrote this code
def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            messages.error(request, user_form.errors)
            messages.error(request, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            # log the user in and go to the homepage
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password is incorrect")
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    # log the user our and return success message
    logout(request)
    messages.success(request, 'you have been logged out')
    return redirect('/')


@login_required
def user_search(request):
    context = {}
    search_result = None
    if request.method == "POST":
        search = request.POST.get('search')
        if search:
            # filter AppUser whose user's username contains the search query (case-insensitive)
            search_result = AppUser.objects.filter(user__username__icontains=search).exclude(user=request.user)
        else:
            # if search bar is blank, retrieve all AppUsers excluding the current user
            search_result = AppUser.objects.all().exclude(user=request.user)

        result_with_pfp = []

        for user in search_result:
            if user.pfp:
                result_with_pfp.append((user.user, user.pfp.url))
            else:
                result_with_pfp.append((user.user, None))

    context = {
        'search_result': result_with_pfp,
    }

    return render(request, "search.html", context)

def home(request, *args, **kwargs):
    context = {}
    user = request.user
    # check if request method is post and that the user is authenticated
    if request.method == "POST" and user.is_authenticated:
        # get the user post form
        post_form = PostsForm(request.POST, request.FILES)
        context['post_form'] = post_form

        # check if the post_form is valid
        if post_form.is_valid():
            # set the user field of the new post
            post_form.instance.user = user
            # save the form, including the image, to the database
            post_form.save()
            messages.success(request, 'Successfully uploaded a new post')
            return HttpResponseRedirect("/")
        else:
            messages.success(request, post_form.errors)
            return HttpResponseRedirect("/")

    # if the user is authenticated
    if user.is_authenticated:
        post_form = PostsForm()
        context['post_form'] = post_form

        # get the list of users the current user is following
        followings_list = [user]  # initialize with the current user
        following_objects = Followers.objects.filter(follower=user)
        followings_list.extend(following_objects.values_list('user', flat=True))

        posts = Posts.objects.filter(user__in=followings_list).order_by('-id')
        context['posts'] = posts

        # get all the profiles of the following list to get their profile images later on
        profiles = AppUser.objects.filter(user__in=followings_list)
        profiles_with_pfp = []
        for profile in profiles:
            if profile.pfp:
                profiles_with_pfp.append((profile, profile.pfp.url))
            else:
                profiles_with_pfp.append((profile, None))

        # context['profiles'] = profiles
        context['profiles'] = profiles_with_pfp

    return render(request, "home.html", context)

@login_required
def profile(request):
    context = {}
    user = request.user
    profile = AppUser.objects.get(user=user)
    #get all current user's post
    posts = Posts.objects.filter(user=user).order_by('-id')
    #get user's followers & followings details
    followers = Followers.objects.filter(user=user)
    followers_with_pfp = []
    for follower in followers:
        follower_profile = AppUser.objects.get(user=follower.follower)
        if follower_profile.pfp:
            followers_with_pfp.append((follower, follower_profile.pfp.url))
        else:
            followers_with_pfp.append((follower, None))

    followings = Followers.objects.filter(follower=user)
    followings_with_pfp = []
    for following in followings:
        following_profile = AppUser.objects.get(user=following.user)
        if following_profile.pfp:
            followings_with_pfp.append((following, following_profile.pfp.url))
        else:
            followings_with_pfp.append((following, None))

    context['profile'] = profile
    context['posts'] = posts
    # context['followers'] = followers
    context['followers'] = followers_with_pfp
    # context['followings'] = followings
    context['followings'] = followings_with_pfp
    return render(request, "profile.html", context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            # return success message
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile')
        else:
            # else return error message
            messages.error(request, 'There was an error when updating your profile')
            return redirect('edit_profile')
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
        }
    return render(request, 'edit_profile.html', context)

@login_required
def viewing(request, username):
    context = {}
    context['username'] = username
    # convert to object to be read when filtering as it is a foreign key in the models
    username = User.objects.get(username=username)
    # get viewing user's details
    profile = AppUser.objects.get(user=username)
    context['profile'] = profile
    # redirect back to own profile if own username is clicked
    if username == request.user:
        return redirect('profile')
    else:
        # when follow button is pressed
        if request.method == 'POST':
            if Followers.objects.filter(user=username, follower=request.user):
                Followers.objects.filter(user=username, follower=request.user).delete()
                isFollowing = False
            else:
                Followers.objects.create(user=username, follower=request.user)
                isFollowing = True

            context['isFollowing'] = isFollowing

            followers = Followers.objects.filter(user=username)
            followers_with_pfp = []
            for follower in followers:
                follower_profile = AppUser.objects.get(user=follower.follower)
                if follower_profile.pfp:
                    followers_with_pfp.append((follower, follower_profile.pfp.url))
                else:
                    followers_with_pfp.append((follower, None))
            context['followers'] = followers_with_pfp

            followings = Followers.objects.filter(follower=username)
            followings_with_pfp = []
            for following in followings:
                following_profile = AppUser.objects.get(user=following.user)
                if following_profile.pfp:
                    followings_with_pfp.append((following, following_profile.pfp.url))
                else:
                    followings_with_pfp.append((following, None))
            context['followings'] = followings_with_pfp

            posts = Posts.objects.filter(user__username=username).order_by('-id')
            context['posts'] = posts
            return redirect('viewing', username=username)

        else:
            if Followers.objects.filter(user=username, follower=request.user):
                isFollowing = True
            else:
                isFollowing = False

            context['isFollowing'] = isFollowing

            followers = Followers.objects.filter(user=username)
            followers_with_pfp = []
            for follower in followers:
                follower_profile = AppUser.objects.get(user=follower.follower)
                if follower_profile.pfp:
                    followers_with_pfp.append((follower, follower_profile.pfp.url))
                else:
                    followers_with_pfp.append((follower, None))
            context['followers'] = followers_with_pfp

            followings = Followers.objects.filter(follower=username)
            followings_with_pfp = []
            for following in followings:
                following_profile = AppUser.objects.get(user=following.user)
                if following_profile.pfp:
                    followings_with_pfp.append((following, following_profile.pfp.url))
                else:
                    followings_with_pfp.append((following, None))
            context['followings'] = followings_with_pfp

            posts = Posts.objects.filter(user__username=username).order_by('-id')
            context['posts'] = posts

        return render (request, 'viewing.html', context)

@login_required
def chats(request):
    context = {}
    if request.method == "POST":
        chatroomForm = ChatroomForm(request.POST)
        if chatroomForm.is_valid():
            chatroomForm.save()
            chatroom = request.POST['chatroom']
            messages.success(request, 'Chatroom created successfully')
            return redirect('/chats/' + chatroom)
        else:
            messages.error(request, 'There was an error when creating the chatroom')
            return redirect('chats')
    else:
        chatroom = Chatroom.objects.all()
        # show create chatroom form
        chatroomForm = ChatroomForm()
        context['chatroom'] = chatroom
        context['chatroomForm'] = chatroomForm

    return render(request, 'chats.html', context)

@login_required
def chatroom(request, chatroom):
    context = {}
    if request.method == "GET":
        # retrieve and display chat history for the current chatroom
        chat_history = ChatroomMessages.objects.filter(chatroom__chatroom=chatroom).order_by('timestamp')
        context['chatroom'] = chatroom
        context['chat_history'] = chat_history
        return render(request, 'chatroom.html', context)

# def deleteChatroom(request, chatroom):
#     # if user wants to delete the chatroom
#     try:
#         chatroom = Chatroom.objects.get(chatroom = chatroom)
#         chatroom.delete()
#         ChatroomMessages = ChatroomMessages.objects.get(chatroom = chatroom)
#         ChatroomMessages.delete()
#         messages.success(request, 'Chatroom deleted successfully')
#         return redirect('chats')
#     except:
#         messages.error(request, 'There was an error when deleting the chatroom')
#         return redirect('chats')

class AppUserList(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

class AppUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

class PostsList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
# end of code I wrote