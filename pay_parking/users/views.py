from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm

@login_required
def edit_profile(request):
    instance = request.user
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('users:profile')
    return render(request, 'users/user.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')
