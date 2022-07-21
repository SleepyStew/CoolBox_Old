from django.urls import path

from . import views

urlpatterns = [
    path('oauth/login', views.discord_oauth_login, name='login'),
]