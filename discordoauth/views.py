from django.shortcuts import render, redirect


# Create your views here.


def discord_oauth_login(request):
    return redirect('/')