from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from bgtrbl.apps.trblcms.models import Category, Article

from allauth.account.forms import LoginForm

from django.conf import settings

def _add_modal_login_form(user, context):
    if not user.is_authenticated():
        context['modal_login_form'] = LoginForm()


def home(request):
    context = dict()

    # 이미지 임시 홀더 (design_comps/img)
    import os
    IMG_DIR = os.path.join(settings.MEDIA_ROOT,'design_comps','img')
    context['images']=["/media/design_comps/img/{}".format(_) for _ in os.listdir(IMG_DIR) if not _.startswith(".")]

    return render(request, 'main/home.html', context)


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})


def magazine(request):
    magazin_category = get_object_or_404(Category, title='Magazin')
    context = {sub.title: sub.article_set.all() for sub in magazin_category.get_descendants()}
    _add_modal_login_form(request.user, context)
    return render(request, 'front_magazine.html', context)


def forum(request):
    forum_category = get_object_or_404(Category, title="Forum")
    context = {sub.title: sub.article_set.all() for sub in forum_category.get_descendants()}
    return render(request, 'front_forum.html', context)

    def get_context_data(self, **kwargs):
        context = super(forum, self).get_context_data(**kwargs)
        _add_modal_login_form(self.request.user, context)
        return context
