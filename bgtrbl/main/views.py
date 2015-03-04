from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from bgtrbl.apps.trblcms.models import Article, Category

def home(request):
    return render(request, 'main/home.html', {})


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})

class magazine(ListView):
    model = Article
    template = "front_magazine.html" 
    queryset = Article.objects.filter(category= Category.objects.get(pk=2))

class forum(ListView):
    model = Article
    template = "front_forum.html"
    queryset = Article.objects.filter(category= Category.objects.get(pk=3))


    
