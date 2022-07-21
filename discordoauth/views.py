from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.


def discord_oauth_login(request):
    code = request.GET.get('code')
    print(code)
    return JsonResponse({'msg': 'Redirected.'})