from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime

# Create your views here.


@login_required
def reminders(request):
    return render(request, 'reminders/reminders.html')


@login_required
def create_reminder(request):
    if request.method == 'POST':
        time = request.POST.get('time')
        timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M')
        return redirect('/reminders/')
    return render(request, 'reminders/create_reminder.html')
