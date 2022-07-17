from django.shortcuts import redirect


def root(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/auth/login')