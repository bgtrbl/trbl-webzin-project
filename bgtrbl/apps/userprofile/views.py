from django.shortcuts import render, redirect

from django.views.generic.detail import DetailView

from .models import UserProfile
from .forms import UserProfileModelForm


class UserProfileDetail(DetailView):
    model = UserProfile
    template_name = 'userprofile/userprofile_detail.html'


def editUserProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = UserProfileModelForm(instance=user_profile)
    return render(request, 'userprofile/edit_userprofile.html', {'form': form})


# login required
def updateUserProfile(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileModelForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('userprofile:my_userprofile')
        # @todo url namespace: main
        return redirect('userprofile:edit_userprofile')
    return redirect('main:home')


# view that displays user profile
# login required
def myUserProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'userprofile/my_userprofile.html', {'user_profile': user_profile})
