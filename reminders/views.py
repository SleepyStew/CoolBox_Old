from django.shortcuts import render

# Create your views here.


def reminders(request):
    return render(request, 'reminders/reminders.html')