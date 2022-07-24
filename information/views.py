from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def information(request):
    return render(request, 'information/information.html')
