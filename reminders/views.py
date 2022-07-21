import time
import threading

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from discordoauth.views import get_discord_user
# Create your views here.

from .models import Reminder


@login_required
def reminders(request):
    print(datetime.now())
    print(datetime.now())
    discordoauthed = request.user.discordoauth_set.exists()
    if discordoauthed:
        discord_user = get_discord_user(request.user)
        discord_full_name = discord_user['username'] + '#' + discord_user['discriminator']
    else:
        return render(request, 'reminders/reminders.html', context={'discordoauthed': discordoauthed})
    reminders = []
    for reminder in Reminder.objects.filter(owner=request.user).order_by('due'):
        reminder.date = datetime.fromtimestamp(reminder.due).strftime('%H:%M %d/%m/%Y')
        reminders.append(reminder)
    return render(request, 'reminders/reminders.html', context={'reminders': reminders, 'discordoauthed': discordoauthed, 'discord_full_name': discord_full_name})


@login_required
def create_reminder(request):
    if request.method == 'POST':
        time = request.POST.get('time')
        date = datetime.strptime(time, '%Y-%m-%d %H:%M')
        due = date.timestamp()
        title = request.POST.get('title')
        if title is None:
            title = 'No title'
        description = request.POST.get('description')
        if description is None:
            description = 'No description'
        reminder = Reminder(owner=request.user, due=due, title=title, description=description)
        reminder.save()
        return redirect('/reminders/')
    return render(request, 'reminders/create_reminder.html')


def reminder_check():
    while True:
        for reminder in Reminder.objects.all():
            if reminder.fulfilled:
                continue
            if reminder.due < datetime.now().timestamp():
                reminder.fulfilled = True
                reminder.save()
                discord_user = get_discord_user(reminder.owner)
                requests.get('http://192.168.50.121:30022/?user=' + discord_user['id'] + '&name=' + reminder.owner.name.split(' ')[0] + '&title=' + reminder.title +
                             '&description=' + reminder.description)
                print("Reminder: " + reminder.title + " has been fulfilled.")
        time.sleep(10)


thread = threading.Thread(target=reminder_check)
thread.setDaemon(True)
thread.start()
