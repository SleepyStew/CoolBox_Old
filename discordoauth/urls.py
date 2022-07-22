from django.urls import path

from . import views

urlpatterns = [
    path('oauth/login/', views.discord_oauth_login, name='login'),
    path('oauth/logout/', views.discord_oauth_logout, name='logout'),
    path('oauth/redirect/', views.discord_oauth_redirect, name='redirect'),
    path('invite/', views.discord_invite, name='invite'),
    path('', views.discord_actions, name='discord'),
]