from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'main/home.html', {})

def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})

def profileView(request):
    return render(request, 'main/allauth_test.html', {})
