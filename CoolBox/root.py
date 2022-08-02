from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def root(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return redirect(reverse('login'))


@require_http_methods(["GET"])
def robots(request):
    robots_txt = """User-agent: Googlebot
Disallow:

User-agent: *
Disallow: /
"""
    return HttpResponse(robots_txt, content_type='text/plain')