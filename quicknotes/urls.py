from django.urls import path

from . import views

urlpatterns = [
    path('', views.quicknotes, name='quick-notes'),
    path('create', views.create_note, name='create'),
    path('delete', views.delete_note, name='delete'),
    path('edit', views.edit_note, name='edit'),
    path('update-order', views.update_note_order, name='update-order'),
]