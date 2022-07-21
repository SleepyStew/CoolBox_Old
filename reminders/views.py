import time
import threading

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime

# Create your views here.

from .models import Reminder


@login_required
def reminders(request):
    reminders = []
    for reminder in Reminder.objects.filter(owner=request.user).order_by('due'):
        reminder.date = datetime.fromtimestamp(reminder.due).strftime('%H:%M %d/%m/%Y')
        reminders.append(reminder)
    return render(request, 'reminders/reminders.html', context={'reminders': reminders})


@login_required
def create_reminder(request):
    if request.method == 'POST':
        time = request.POST.get('time')
        date = datetime.strptime(time, '%Y-%m-%d %H:%M')
        due = date.timestamp()
        title = request.POST.get('title')
        description = request.POST.get('description')
        reminder = Reminder(owner=request.user, due=due, title=title, description=description)
        reminder.save()
        return redirect('/reminders/')
    return render(request, 'reminders/create_reminder.html')


def reminder_check():
    while True:
        for reminder in Reminder.objects.all():
            if reminder.fulfilled:
                continue
            print(reminder.due - time.time())
            if reminder.due < time.time():
                reminder.fulfilled = True
                reminder.save()
                requests.get('http://127.0.0.1:5000/?name=' + reminder.owner.name.split(' ')[0] + '&title=' + reminder.title + '&description=' + reminder.description)
                print("Reminder: " + reminder.title + " has been fulfilled.")
        time.sleep(10)


thread = threading.Thread(target=reminder_check)
thread.setDaemon(True)
thread.start()
