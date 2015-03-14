from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from bgtrbl.apps.trblcms.models import Category, Article

from allauth.account.forms import LoginForm

from django.conf import settings
from endless_pagination.decorators import page_template

from django.template import RequestContext;


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
    return render(request, 'main/home.html', context, context_instance=RequestContext(request))


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})

@page_template('main/front_review_endless.html')
def magazine(request, extra_context=None):
    magazin_category = get_object_or_404(Category, title='Magazin')
    context = {sub.title: sub.article_set.all() for sub in magazin_category.get_descendants()}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, 'main/front_magazine.html', context, context_instance=RequestContext(request))


def forum(request):
    forum_category = get_object_or_404(Category, title="Forum")
    context = {sub.title: sub.article_set.all() for sub in forum_category.get_descendants()}
    return render(request, 'main/front_forum.html', context, context_instance=RequestContext(request))
