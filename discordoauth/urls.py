from django.urls import path

from . import views

urlpatterns = [
    path('oauth/login/', views.discord_oauth_login, name='discord_login'),
    path('oauth/logout/', views.discord_oauth_logout, name='discord_logout'),
    path('oauth/redirect/', views.discord_oauth_redirect, name='discord_redirect'),
    path('invite/', views.discord_invite, name='discord_invite'),
    path('', views.discord_actions, name='discord'),
]