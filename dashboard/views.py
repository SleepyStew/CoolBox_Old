from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/auth/login')


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')