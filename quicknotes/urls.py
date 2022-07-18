from django.urls import path

from . import views

urlpatterns = [
    path('', views.quicknotes, name='quick-notes'),
]