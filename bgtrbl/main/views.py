from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic.detail import DetailView

from .models import UserProfile
from .forms import UserProfileModelForm


def home(request):
    return render(request, 'main/home.html', {})


def allauthTest(request):
    return render(request, 'main/allauth_test.html', {})


class UserProfileDetail(DetailView):
    model = UserProfile
    template_name = 'main/userprofile_detail.html'


def editUserProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = UserProfileModelForm(instance=user_profile)
    return render(request, 'main/edit_userprofile.html', {'form': form})


# login required
def updateUserProfile(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileModelForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('my_userprofile')
        # @todo url namespace: main
        return redirect('edit_userprofile')
    return redirect('main:home')


# view that displays user profile
# login required
def myUserProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'main/my_userprofile.html', {'user_profile': user_profile})
