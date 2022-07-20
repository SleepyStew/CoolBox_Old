from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


@login_required
def reminders(request):
    return render(request, 'reminders/reminders.html')


@login_required
def create_reminder(request):
    return render(request, 'reminders/create_reminder.html')
