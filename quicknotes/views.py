import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Note

# Create your views here.

@login_required
@require_http_methods(["GET"])
def quicknotes(request):
    notes = request.user.note_set.all().order_by('display_id')
    return render(request, 'quicknotes/quicknotes.html', context={'notes': notes})


@login_required
@require_http_methods(["POST"])
def create_note(request):
    if request.method == 'POST':
        note = Note(owner=request.user, content=request.POST.get('content'), display_id=request.user.note_set.all().order_by('display_id').first().display_id - 1)
        note.save()
        return redirect(reverse('quick-notes'))
    return redirect(reverse('root'))


@login_required
@require_http_methods(["POST"])
def delete_note(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['note_id'].isdigit():
            return redirect(reverse('quick-notes'))
        note = Note.objects.get(id=request_data['note_id'])
        if note.owner == request.user:
            note.delete()
            return redirect(reverse('quick-notes'))
    return redirect(reverse('quick-notes'))


@login_required
@require_http_methods(["POST"])
def edit_note(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['note_id'].isdigit():
            return redirect(reverse('quick-notes'))
        if not request_data['note_content']:
            return redirect(reverse('quick-notes'))
        note = Note.objects.get(id=request_data['note_id'])
        if note.owner == request.user:
            note.content = request_data['note_content']
            note.save()
            return redirect(reverse('quick-notes'))
    return redirect(reverse('quick-notes'))


@login_required
@require_http_methods(["POST"])
def update_note_order(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        if not request_data['order']:
            return redirect(reverse('quick-notes'))
        for note_id in request_data['order']:
            if not note_id.isdigit():
                return redirect(reverse('quick-notes'))
        for x in range(len(request_data['order'])):
            note = Note.objects.get(id=request_data['order'][x])
            if note.owner == request.user:
                note.display_id = x + 1
                note.save()

        return redirect(reverse('quick-notes'))
    return redirect(reverse('quick-notes'))