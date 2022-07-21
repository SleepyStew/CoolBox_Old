import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import DiscordOAuth

# Create your views here.


def discord_oauth_login(request):
    if request.user.discordoauth_set.exists():
        return redirect('/')
    return redirect('https://discord.com/api/oauth2/authorize?client_id=999205944133177365&redirect_uri=https%3A%2F%2Fnew.coolbox.lol%2Fdiscord%2Foauth%2Fredirect'
                    '&response_type=code&scope=identify')


def discord_oauth_redirect(request):
    code = request.GET.get('code')
    if code:
        data = {
            'client_id': '999205944133177365',
            'client_secret': 'xvwjk5mDMmDdILyxsftqrS67DxQoBZ9t',
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://new.coolbox.lol/discord/oauth/redirect',
            'scope': 'identify',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://discordapp.com/api/oauth2/token', data=data, headers=headers)
        if response.status_code == 200:
            print(response.json())
            messages.success(request, "Successfully authenticated with Discord.")
            discordoauth = DiscordOAuth(
                user=request.user,
                access_token=response.json()['access_token'],
                refresh_token=response.json()['refresh_token'],
                expires_in=response.json()['expires_in']
            )
            discordoauth.save()
        else:
            messages.error(request, "Failed to authenticate with Discord.")
            print(response.text)
    return redirect('/')


def get_discord_user(user):
    discordoauth = user.discordoauth_set.first()
    if not discordoauth:
        return False
    discord_user = requests.get('https://discordapp.com/api/users/@me', headers={'Authorization': 'Bearer ' + discordoauth.access_token}).json()
    if discord_user:
        return discord_user
    return False