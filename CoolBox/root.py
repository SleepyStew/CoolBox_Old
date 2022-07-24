from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def root(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/auth/login')
