"""CoolBox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from . import root

urlpatterns = [
    path('', root.root),
    path('auth/', include('schoolboxauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('quick-notes/', include('quicknotes.urls')),
    path('information/', include('information.urls')),
    path('reminders/', include('reminders.urls')),
    path('discord/', include('discordoauth.urls')),
    path('admin/', admin.site.urls),
]


def error_404(request, exception):
    return redirect('/')


handler404 = 'CoolBox.urls.error_404'
