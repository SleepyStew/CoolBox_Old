from django.contrib import messages
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import User


# Create your views here.


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('root'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        request_data = {
            'username': username.replace(" ", "."),
            'password': password
        }

        login_request = requests.post("https://schoolbox.donvale.vic.edu.au/api/session", data=request_data)

        if login_request.status_code == 400 or login_request.status_code == 401:
            messages.error(request, "Incorrect username or password.")
        elif login_request.status_code == 200:
            id = login_request.text.split('= {"id":')[1].split("\"")[0][:-1]
            name = login_request.text.split(',"fullName":"')[1].split("\"")[0]

            user = User.objects.filter(id=id).first()
            if user:
                user.cookie = str(login_request.cookies.get('PHPSESSID'))
                user.username = username
                user.save()
                messages.success(request, f"Welcome back, {user.name.split(' ')[0]}!")
            else:
                user = User(id=id, cookie=str(login_request.cookies.get('PHPSESSID')), name=name)
                user.save()
                messages.success(request, f"Welcome to the CoolBox Dashboard, {user.name.split(' ')[0]}!")

            auth_login(request, user)
            return redirect(reverse('root'))

    return render(request, 'schoolboxauth/login.html')


@require_http_methods(["GET"])
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect(reverse('root'))
