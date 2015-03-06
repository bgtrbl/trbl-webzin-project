from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from bgtrbl.apps.trblcms.models import Category, Article

def home(request):
    return render(request, 'main/home.html', {})


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})


class magazine(ListView):
    model = Category
    template_name = "front_magazine.html"
    context_object_name = "category"
    queryset = Category.objects.filter(parent=Category.objects.filter(title='Magazin'))

    def get_context_data(self, **kwargs):
        context = super(magazine, self).get_context_data(**kwargs)
        for i in self.queryset:
            context[i.title] = Article.objects.filter(category=i)
        return context


class forum(ListView):
    model = Article
    template_name = "front_forum.html"
    queryset = Article.objects.filter(category=Category.objects.get(pk=3))[:20]
