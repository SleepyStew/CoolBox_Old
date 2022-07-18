from django.shortcuts import render

# Create your views here.


def quicknotes(request):
    return render(request, 'quicknotes/quicknotes.html')
