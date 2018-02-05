import requests
import re
from bs4 import BeautifulSoup
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
from datetime import datetime
import datetime

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

"""def init_crawl_codechef(x):
    url = "https://www.codechef.com/recent/user?page=0&user_handle=" + x + "&_=1510300136417"
    # mathecodician
    # sagar_sam
    # print(url)
    pages = []
    r = requests.get(url)
    today = datetime.date.today()
    soup = BeautifulSoup(r.content, "html.parser")
    output2 = " "
    for j in soup.text[12:]:
        if j != ",":
            output2 += j
        else:
            break

    output2 = int(output2)
    # print(output2)
    count = 0
    accepted = 0
    count2 = 0
    stop = 0
    num_of_pages = 0
    for a in range(0, output2):
        # for a in range(0, 10):
        url = "https://www.codechef.com/recent/user?page=" + str(a) + "&user_handle=" + x + "&_=1510300136417"
        pages.append(url)

    for i in pages:
        count += 1

    for item in pages:
        num_of_pages += 1
        r = requests.get(item)
        soup = BeautifulSoup(r.content, "html.parser")
        g_data3 = soup.find_all("td")
        count = 0
        for item3 in g_data3:
            if (count % 4 == 0):
                output = " "
                output = item3.contents[0]
                wordList = re.sub("[^\w]", " ", output).split()
                if wordList.__len__() > 2:
                    streee = wordList[2]
                    if streee == 'ago':
                        case = today
                        case = case.replace(case.year - 2000)
                        case = case.strftime('%d\/%m\/%Y')
                        output = "12:12 PM " + case + "<\/td>"

            elif count % 2 == 0:
                flag = 0
                points = []
                for j in item3.contents[0]:
                    flag += 1
                if (flag == 6):
                    counter = 0
                    for j in item3.contents[0]:
                        counter += 1
                        if (counter == 3):
                            points.append(str(j))
                if (points == ['100']):
                    accepted += 1
                    x = output
                    x = int(output[9:11])
                    y = int(output[13:15])
                    z = 2000
                    z = z + int(output[17:19])
                    someday = datetime.date(z, y, x)  # .strftime('%Y-%m-%d')
                    some2 = datetime.date(z, y, x).strftime('%Y-%m-%d')
                    pastday = today - datetime.timedelta(days=11)
                    past = pastday.strftime('%Y-%m-%d')
                    if (some2 > past):
                        count2 += 1
                    else:
                        flag = 1
                    output = " "
            count += 1
            if (stop == 1):
                break
        if (stop == 1):
            break
    output = int(count2)
    init_codechef_rating = output
    return init_codechef_rating"""

def init_crawl_spoj(input):
    pages = []
    count = 0
    count2 = 0
    output = " "
    stop = 0
    flag5 = 1
    today = datetime.date.today()
    url5 = 'http://www.spoj.com/users/' + input
    r5 = requests.get(url5)
    soup5 = BeautifulSoup(r5.content, "html.parser")
    x5 = soup5.find("div", {"class": "col-md-3"})
    if x5 is None:
        flag5 = 0

    if flag5 is 1:
        for a in range(0, 5):
            url = 'http://www.spoj.com/status/' + input + '/all/start=' + str(a * 20)
            pages.append(url)
        for item in pages:
            page = requests.get(item)
            soup = BeautifulSoup(page.content, "html.parser")
            artist_name_list = soup.find_all("tr", {"class": "kol1"})
            artist_name_list2 = soup.find_all("tr", {"class": "kol2"})
            artist_name_list3 = soup.find_all("tr", {"class": "kol3"})
            for i in artist_name_list:
                # print(i.contents[3].text)
                count += 1
                for j in i.contents[3].text:
                    if j != " ":
                        output += j
                    else:
                        output = output.strip()
                        # print(output)
                        x = int(output[:4])
                        y = int(output[5:7])
                        z = int(output[8:10])
                        someday = datetime.date(x, y, z)  # .strftime('%Y-%m-%d')
                        some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                        pastday = today - datetime.timedelta(days=30)
                        past = pastday.strftime('%Y-%m-%d')
                        if (some2 > past):
                            count2 += 1
                        else:
                            stop = 1
                        output = " "
                        break
                if (stop == 1):
                    break
            for i in artist_name_list2:
                # print(i.contents[3].text)
                count += 1
                for j in i.contents[3].text:
                    if j != " ":
                        output += j
                    else:
                        output = output.strip()
                        # print(output)
                        x = int(output[:4])
                        y = int(output[5:7])
                        z = int(output[8:10])
                        someday = datetime.date(x, y, z)  # .strftime('%Y-%m-%d')
                        some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                        pastday = today - datetime.timedelta(days=10)
                        past = pastday.strftime('%Y-%m-%d')
                        if (some2 > past):
                            count2 += 1
                        else:
                            stop = 1
                        output = " "
                        break
                if (stop == 1):
                    break
            for i in artist_name_list3:
                # print(i.contents[3].text)
                count += 1
                for j in i.contents[3].text:
                    if j != " ":
                        output += j
                    else:
                        output = output.strip()
                        # print(output)
                        x = int(output[:4])
                        y = int(output[5:7])
                        z = int(output[8:10])
                        someday = datetime.date(x, y, z)  # .strftime('%Y-%m-%d')
                        some2 = datetime.date(x, y, z).strftime('%Y-%m-%d')
                        pastday = today - datetime.timedelta(days=10)
                        past = pastday.strftime('%Y-%m-%d')
                        if (some2 > past):
                            count2 += 1
                        else:
                            stop = 1
                        output = " "
                        break
                if (stop == 1):
                    break
            if (stop == 1):
                break
    output = int(count2)
    init_spoj_rating = output
    return init_spoj_rating


def signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            profile = Profile.objects.create(username=user, image="nullasofnow")
            profile.hacker_earth_username = request.POST['hacker_earth_username']
            profile.spoj_username = request.POST['spoj_username']
            profile.codechef_username = request.POST['codechef_username']
            profile.save()
            #profile.codechef_rating = init_crawl_codechef(profile.codechef_username)
            profile.spoj_rating = init_crawl_spoj(profile.spoj_username)
            #profile.hacker_earth = init_crawl_hackerearth(profile.hacker_earth_rating)
            profile.save()
            login(request, user)
            return redirect('main:profile', username=user.username)
    return render(request, 'main/signup.html', {"form": Signupform(request.POST or None)})

def LeaderBoard(request):

    profiles = Profile.objects.all()
    for profile in profiles:
        try:
            total = int(profile.codechef_rating + profile.spoj_rating + profile.hacker_earth_rating)
            profile.total_questions = total
            profile.save()
        except ValueError:
            pass

    return render(request, 'main/leaderboard.html', {"profiles": Profile.objects.all()})
    #spoj = yamini_96 , baqir96 , kshtjgpt15
    #hacherearth = yami96 , sagar_sam , nazar.class , babe
    #codechef = dpraveen , ritesh_gupta , topcoder_7

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
