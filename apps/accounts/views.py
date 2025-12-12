"""
Views for the accounts application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserProfileForm


@login_required
def profile_view(request):
    """Display and edit user profile."""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


def registration_pending_view(request):
    """View shown after registration pending approval."""
    return render(request, 'accounts/registration_pending.html')
