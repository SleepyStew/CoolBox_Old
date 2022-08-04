import time
import threading
from os import environ

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from discordoauth.models import DiscordOAuth
# Create your views here.
from discordoauth.views import get_discord_user

from .models import Reminder


@login_required
@require_http_methods(["GET"])
def reminders(request):
    discord_authenticated = request.user.discordoauth_set.exists()
    reminders = []
    for reminder in Reminder.objects.filter(owner=request.user).order_by('due'):
        reminder.date = datetime.fromtimestamp(reminder.due).strftime('%H:%M %d/%m/%Y')
        reminders.append(reminder)
    return render(request, 'reminders/reminders.html', context={'reminders': reminders, 'discord_authenticated': discord_authenticated})


@login_required
@require_http_methods(["GET", "POST"])
def create_reminder(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title == '' or title is None:
            return redirect(reverse('create_reminder'))
        time = request.POST.get('time')
        if time == '' or time is None:
            return redirect(reverse('create_reminder'))
        date = datetime.strptime(time, '%Y-%m-%d %H:%M')
        due = date.timestamp()
        description = request.POST.get('description')
        if description == '' or description is None:
            description = 'No description'
        repeat = request.POST.get('repeat')
        if repeat is None or not repeat.isdigit() or int(repeat) not in [0, 1, 2, 3]:
            repeat = 0
        else:
            repeat = int(repeat)
        reminder = Reminder(owner=request.user, due=due, title=title, description=description, repeat=repeat)
        reminder.save()
        messages.success(request, 'Reminder successfully created!')
        return redirect(reverse('reminders'))
    return render(request, 'reminders/create_reminder.html')


@login_required
@require_http_methods(["POST"])
def delete_reminder(request):
    id = request.POST.get('id')
    if id is None or id == '':
        return redirect(reverse('reminders'))
    try:
        reminder = Reminder.objects.get(id=id)
    except Reminder.DoesNotExist:
        return redirect(reverse('reminders'))
    if reminder.owner == request.user:
        reminder.delete()
        messages.success(request, 'Reminder successfully deleted!')
    return redirect(reverse('reminders'))


@login_required
@require_http_methods(["GET", "POST"])
def edit_reminder(request, id):
    if request.method == 'POST':
        try:
            reminder = Reminder.objects.get(id=id)
        except Reminder.DoesNotExist:
            return redirect(reverse('reminders'))
        if reminder.owner == request.user:
            title = request.POST.get('title')
            if title == '' or title is None:
                return redirect(reverse('edit_reminder') + id)
            time = request.POST.get('time')
            if time == '' or time is None:
                return redirect(reverse('edit_reminder') + id)
            date = datetime.strptime(time, '%Y-%m-%d %H:%M')
            due = date.timestamp()
            description = request.POST.get('description')
            if description == '' or description is None:
                description = 'No description'
            repeat = request.POST.get('repeat')
            if repeat is None or not repeat.isdigit() or int(repeat) not in [0, 1, 2, 3]:
                repeat = 0
            else:
                repeat = int(repeat)
            reminder.title = title
            reminder.due = due
            reminder.description = description
            reminder.repeat = repeat
            reminder.save()
            messages.success(request, 'Reminder successfully edited!')
            return redirect(reverse('reminders'))
    else:
        try:
            reminder = Reminder.objects.get(id=id)
        except Reminder.DoesNotExist:
            return redirect(reverse('reminders'))
        if reminder.owner != request.user:
            return redirect(reverse('reminders'))
        if request.method == 'POST':
            pass
        return render(request, 'reminders/edit_reminder.html', context={'reminder': reminder})


def reminder_check():
    while True:
        time.sleep(10)
        for reminder in Reminder.objects.all():
            if reminder.due < datetime.now().timestamp():
                discord_user = get_discord_user(reminder.owner)
                if discord_user:
                    requests.get(
                        environ.get('DISCORD_BOT_URL') + '?user=' + discord_user['id'] + '&name=' + reminder.owner.name.split(' ')[0] + '&title=' + reminder.title +
                        '&description=' + reminder.description)
                print("Reminder: " + reminder.title + " has been fulfilled.")
                if reminder.repeat == 0:
                    reminder.delete()
                elif reminder.repeat == 1:
                    reminder.due = reminder.due + 86400
                    reminder.save()
                elif reminder.repeat == 2:
                    reminder.due = reminder.due + 604800
                    reminder.save()
                elif reminder.repeat == 3:
                    reminder.due = reminder.due + 31536000
                    reminder.save()


thread = threading.Thread(target=reminder_check)
thread.setDaemon(True)
thread.start()
