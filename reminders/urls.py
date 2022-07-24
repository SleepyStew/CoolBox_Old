from django.urls import path

from . import views

urlpatterns = [
    path('', views.reminders, name='reminders'),
    path('create/', views.create_reminder, name='create_reminder'),
    path('delete/', views.delete_reminder, name='delete_reminder'),
    path('edit/<int:id>/', views.edit_reminder, name='edit_reminder'),
]