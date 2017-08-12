from .form import Loginform, Signupform
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse, JsonResponse
from .models import Profile, Activity, View, Post
from discussions.models import Question
from django.db.models import Q, Case, When, Sum
from django import forms


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.method == "GET":
                if request.GET["next"]:
                    return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('main:profile', kwargs={'username': user.username}))
    return render(request, 'main/login.html', {"form": Loginform(request.POST or None)})


def signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            profile = Profile.objects.create(username=user, image="nullasofnow")
            profile.save()
            login(request, user)
            return redirect('main:profile', username=user.username)
    return render(request, 'main/signup.html', {"form": Signupform(request.POST or None)})


def profile(request, username):
    if request.user.username == username:
        profile = get_object_or_404(Profile, username=User.objects.get(username=username))
        return render(request, 'main/profile.html', {"profile": profile})
    elif request.user.username is not None:
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(username=User.objects.get(username=username))
        if not View.objects.filter(user=user, ip=get_client_ip(request)).exists():
            View.objects.create(user=user, ip=get_client_ip(request)).save()
            profile.views += 1
            profile.save()
        return render(request, 'main/profile.html', {"profile": profile, "user": user})


def index(request):
    return render(request, 'main/home.html', {"posts": Post.objects.all()[:3],
                                              "users": User.objects.annotate(points=Sum('profile__points')).order_by(
                                                  '-points')[:5], "questions": Question.objects.all()})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def logout_view(request):
    logout(request)
    return redirect('main:index')


def activity(request, username):
    user = get_object_or_404(User, username=username)
    Activity.objects.filter(Q(on_username=user) | Q(by_username=user))
    return render(request, 'main/activity.html',
                  {"activities": Activity.objects.filter(Q(on_username=user) | Q(by_username=user)), "user": user})


def activity_all(request):
    return render(request, 'main/activity_all.html', {"activities": Activity.objects.all()})


def posts(request):
    return render(request, 'main/posts.html', {"posts": Post.objects.all()})


def post(request, id):
    return render(request, 'main/post.html', {"post": Post.objects.get(id=id[1:])})


def about(request):
    return render(request, 'main/base.html')


def search(request):
    q = request.GET['q']
    return render(request, 'main/search.html', {"users": User.objects.filter(
        Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)),
        "discussions": Question.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(
                username__username__icontains=q)),
        "posts": Post.objects.filter(Q(username__username__icontains=q) | Q(title__icontains=q))})
