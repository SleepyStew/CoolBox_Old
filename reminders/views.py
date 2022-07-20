from django.shortcuts import render

# Create your views here.


def reminders(request):
    return render(request, 'reminders/reminders.html')


def create_reminder(request):
    return render(request, 'reminders/create_reminder.html')
