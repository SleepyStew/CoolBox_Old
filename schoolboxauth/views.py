from django.contrib import messages
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print("test")

        request_data = {
            'username': username.replace(" ", "."),
            'password': password
        }

        login_request = requests.post("https://schoolbox.donvale.vic.edu.au/api/session", data=request_data)

        print("test1")

        print(username)
        print(password)

        if login_request.status_code == 400 or login_request.status_code == 401:
            messages.error(request, "Incorrect username or password.")
        elif login_request.status_code == 200:
            id = login_request.text.split('= {"id":')[1].split("\"")[0][:-1]
            name = login_request.text.split(',"fullName":"')[1].split("\"")[0]

            user = User.objects.filter(id=id).first()
            if user:
                user.cookie = str(login_request.cookies.get('PHPSESSID'))
                user.username = username
                print("hey12")
                user.save()
            else:
                user = User(id=id, cookie=str(login_request.cookies.get('PHPSESSID')), name=name)
                print("hey")
                user.save()

            auth_login(request, user)
            return redirect('/')

    return render(request, 'schoolboxauth/login.html')


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('/')