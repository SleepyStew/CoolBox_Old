import time
from os import environ

import requests
import threading
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from CoolBox.settings import APP_URL
from .models import DiscordOAuth

# Create your views here.


@login_required
@require_http_methods(["GET"])
def discord_oauth_login(request):
    if request.user.discordoauth_set.exists():
        return redirect(reverse('root'))
    return redirect('https://discord.com/api/oauth2/authorize?client_id=999205944133177365&redirect_uri=' + APP_URL.replace('/', '%2F').replace(':', '%3A') + '%2Fdiscord%2Foauth%2Fredirect&response_type=code&scope=identify')


@login_required
@require_http_methods(["GET"])
def discord_oauth_redirect(request):
    code = request.GET.get('code')
    if code:
        data = {
            'client_id': '999205944133177365',
            'client_secret': environ.get("CLIENT_SECRET"),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': APP_URL + '/discord/oauth/redirect',
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
                expires=time.time() + response.json()['expires_in'] - 600
            )
            discordoauth.save()
        else:
            messages.error(request, "Failed to authenticate with Discord.")
            print(response.text)
    return redirect(reverse('discord'))


def get_discord_user(user):
    discordoauth = user.discordoauth_set.first()
    if not discordoauth:
        return False
    discord_user = requests.get('https://discordapp.com/api/users/@me', headers={'Authorization': 'Bearer ' + discordoauth.access_token})
    if discord_user.status_code == 200:
        return discord_user.json()
    return False


@login_required
@require_http_methods(["GET"])
def discord_actions(request):
    discord_user = get_discord_user(request.user)
    if discord_user is not False:
        discord_name = discord_user['username'] + '#' + discord_user['discriminator']
        return render(request, 'discordoauth/discordactions.html', context={'discord_user': discord_user, 'discord_name': discord_name})
    return render(request, 'discordoauth/discordactions.html', {'discord_user': discord_user})


@login_required
@require_http_methods(["GET"])
def discord_invite(request):
    return redirect('https://discord.com/invite/86f8YEtTa6')


@login_required
@require_http_methods(["GET"])
def discord_oauth_logout(request):
    if request.user.discordoauth_set.exists():
        for discordoauth in request.user.discordoauth_set.all():
            discordoauth.delete()
        messages.success(request, "Successfully unlinked Discord account.")
    return redirect(reverse('discord'))


def refresh_token(user):
    data = {
        'client_id': '999205944133177365',
        'client_secret': environ.get("CLIENT_SECRET"),
        'grant_type': 'refresh_token',
        'refresh_token': user.refresh_token,
        'scope': 'identify',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discordapp.com/api/oauth2/token', data=data, headers=headers)
    if response.status_code == 200:
        print(response.json())
        user.access_token = response.json()['access_token']
        user.expires = time.time() + response.json()['expires_in'] - 600
        user.refresh_token = response.json()['refresh_token']
        user.save()
        return True
    return False


def refresh_tokens():
    while True:
        time.sleep(60)
        for discordoauth in DiscordOAuth.objects.all():
            if time.time() > discordoauth.expires:
                if refresh_token(discordoauth):
                    print("Refreshed token for " + get_discord_user(discordoauth.user)['username'] + '#' + get_discord_user(discordoauth.user)['discriminator'])
                else:
                    print("Failed to refresh token for " + str(discordoauth.user))
                    discordoauth.delete()


thread = threading.Thread(target=refresh_tokens)
thread.setDaemon(True)
thread.start()
