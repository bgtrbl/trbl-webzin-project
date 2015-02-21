from django.shortcuts import render
from django.http import HttpResponse
from ckeditor.widgets import CKEditorWidget  # @? wiget 을 여기다가 임포트?? 모델에다가 하는거 아님??

from .forms import ArticleModelForm, CkeditorTestForm


def formTest(request):
    if request.method == 'POST':
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            output = ''
            for k, v in form.cleaned_data.items():
                output += "{}: {}<br />".format(k, v)
            return HttpResponse("Succeed<br />"+output)
    else:
        # initial attr gives a prepopulated form
        form = ArticleModelForm(initial={'category': None})
    return render(request, 'trblcms/form_test.html', {'form': form})


def ckeditorTest(request):
    if request.method == 'POST':
        form = CkeditorTestForm(request.POST)
        if form.is_valid():
            return HttpResponse("good")
    else:
        form = CkeditorTestForm()
    return render(request, 'trblcms/ckeditor_test.html', {'form': form})
