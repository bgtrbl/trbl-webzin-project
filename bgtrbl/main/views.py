from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from bgtrbl.apps.trblcms.models import Category, Article

from allauth.account.forms import LoginForm


def _add_modal_login_form(user, context):
    if not user.is_authenticated():
        context['modal_login_form'] = LoginForm()


def home(request):
    context = dict()
    _add_modal_login_form(request.user, context)
    return render(request, 'main/home.html', context)


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})


class Magazine(ListView):
    model = Category
    template_name = "front_magazine.html"
    context_object_name = "category"
    queryset = Category.objects.filter(parent=Category.objects.get(title='Magazin'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _add_modal_login_form(self.request.user, context)
        for i in self.queryset:
            context[i.title] = Article.objects.filter(category=i)
        return context


class Forum(ListView):
    model = Article
    template_name = "front_forum.html"
    queryset = Article.objects.filter(category=Category.objects.get(pk=3))[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _add_modal_login_form(self.request.user, context)
        return context
