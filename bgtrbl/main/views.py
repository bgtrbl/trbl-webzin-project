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
    i_1 = ["chimney02.jpg", "copy_0_piu09.jpg", "hikarimachi01.jpg",
    "hikarimachi10.jpg", "set01.jpg", "set04.jpg"]
    i_2 = ["tumblr_lpp3nwMKeG1qzm9x1o1_500.jpg",
    "tumblr_lqodmwu1Bc1qkajw3o1_500.jpg",
    "tumblr_lsmept3KWX1qa8l9bo1_500.jpg", "tumblr_lta828HHqO1qau50i.jpg"]
    i_3 = ["superthumb.gif", "tumblr_kwu8hsmk3Z1qzirnvo1_500.png",
    "tumblr_kwu8hsmk3Z1qzirnvo1_500.png",
    "tumblr_kx1nmq9ihk1qa4rvko1_400.png",
    "tumblr_lmyk6v85ho1qla8s3o1_500.jpg"]

    context['images'] = [ "/media/design_comps/img/{}".format(_) for _ in i_1 ]
    _add_modal_login_form(request.user, context)
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
