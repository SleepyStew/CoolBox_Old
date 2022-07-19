import json

from django.shortcuts import render, redirect
from .models import Note

# Create your views here.


def quicknotes(request):
    notes = request.user.note_set.all().order_by('display_id')
    return render(request, 'quicknotes/quicknotes.html', context={'notes': notes})


def create_note(request):
    if request.method == 'POST':
        note = Note(owner=request.user, content=request.POST.get('content'))
        note.save()
        return redirect('/quick-notes/')
    return redirect('/')


def delete_note(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['note_id'].isdigit():
            return redirect('/quick-notes/')
        note = Note.objects.get(id=request_data['note_id'])
        if note.owner == request.user:
            note.delete()
            return redirect('/quick-notes/')
    return redirect('/quick-notes/')


def edit_note(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['note_id'].isdigit():
            return redirect('/quick-notes/')
        if not request_data['note_content']:
            return redirect('/quick-notes/')
        note = Note.objects.get(id=request_data['note_id'])
        if note.owner == request.user:
            note.content = request_data['note_content']
            note.save()
            return redirect('/quick-notes/')
    return redirect('/quick-notes/')


def update_note_order(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['order']:
            return redirect('/quick-notes/')
        for note_id in request_data['order']:
            if not note_id.isdigit():
                return redirect('/quick-notes/')
        for x in range(len(request_data['order'])):
            note = Note.objects.get(id=request_data['order'][x])
            if note.owner == request.user:
                note.display_id = x
                note.save()

        return redirect('/quick-notes/')
    return redirect('/quick-notes/')