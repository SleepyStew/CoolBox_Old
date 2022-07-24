from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def root(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return redirect(reverse('login'))
