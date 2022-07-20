from django.urls import path

from . import views

urlpatterns = [
    path('', views.reminders, name='reminders'),
    path('create/', views.create_reminder, name='create_reminder'),
]