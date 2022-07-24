import time
import threading

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import get_object_or_404
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
@require_http_methods(["POST"])
def create_reminder(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title == '' or title is None:
            return redirect('/reminders/create')
        time = request.POST.get('time')
        if time == '' or time is None:
            return redirect('/reminders/create')
        date = datetime.strptime(time, '%Y-%m-%d %H:%M')
        due = date.timestamp()
        description = request.POST.get('description')
        if description == '' or description is None:
            description = 'No description'
        reminder = Reminder(owner=request.user, due=due, title=title, description=description)
        reminder.save()
        messages.success(request, 'Reminder successfully created!')
        return redirect('/reminders/')
    return render(request, 'reminders/create_reminder.html')


@login_required
@require_http_methods(["POST"])
def delete_reminder(request):
    id = request.POST.get('id')
    if id is None or id == '':
        return redirect('/reminders/')
    try:
        reminder = Reminder.objects.get(id=id)
    except Reminder.DoesNotExist:
        return redirect('/reminders/')
    if reminder.owner == request.user:
        reminder.delete()
        messages.success(request, 'Reminder successfully deleted!')
    return redirect('/reminders/')


@login_required
@require_http_methods(["GET", "POST"])
def edit_reminder(request, id):
    if request.method == 'POST':
        try:
            reminder = Reminder.objects.get(id=id)
        except Reminder.DoesNotExist:
            return redirect('/reminders/')
        if reminder.owner == request.user:
            title = request.POST.get('title')
            if title == '' or title is None:
                return redirect('/reminders/edit/' + id)
            time = request.POST.get('time')
            if time == '' or time is None:
                return redirect('/reminders/edit/' + id)
            date = datetime.strptime(time, '%Y-%m-%d %H:%M')
            due = date.timestamp()
            description = request.POST.get('description')
            if description == '' or description is None:
                description = 'No description'
            reminder.title = title
            reminder.due = due
            reminder.description = description
            reminder.save()
            messages.success(request, 'Reminder successfully edited!')
            return redirect('/reminders/')
    else:
        try:
            reminder = Reminder.objects.get(id=id)
        except Reminder.DoesNotExist:
            return redirect('/reminders/')
        if reminder.owner != request.user:
            return redirect('/reminders/')
        if request.method == 'POST':
            pass
        return render(request, 'reminders/edit_reminder.html', context={'reminder': reminder})


def reminder_check():
    while True:
        for reminder in Reminder.objects.all():
            if reminder.fulfilled:
                continue
            if reminder.due < datetime.now().timestamp():
                reminder.fulfilled = True
                reminder.save()
                discord_user = get_discord_user(reminder.owner)
                if not discord_user:
                    continue
                requests.get('http://192.168.50.121:30022/?user=' + discord_user['id'] + '&name=' + reminder.owner.name.split(' ')[0] + '&title=' + reminder.title +
                             '&description=' + reminder.description)
                print("Reminder: " + reminder.title + " has been fulfilled.")
                reminder.delete()
        time.sleep(10)


thread = threading.Thread(target=reminder_check)
thread.setDaemon(True)
thread.start()
