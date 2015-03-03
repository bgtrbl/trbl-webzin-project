from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic.detail import DetailView


def home(request):
    return render(request, 'main/home.html', {})


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})
