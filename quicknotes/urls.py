from django.urls import path

from . import views

urlpatterns = [
    path('', views.quicknotes, name='quick-notes'),
    path('create', views.create_note, name='create_quick-note'),
    path('delete', views.delete_note, name='delete_quick-note'),
    path('edit', views.edit_note, name='edit_quick-note'),
    path('update-order', views.update_note_order, name='update-order_quick-note'),
]