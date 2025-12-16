"""
Views for the accounts application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserProfileForm
from apps.common.forms import AddressForm


@login_required
def profile_view(request):
    """Display and edit user profile."""
    user = request.user
    profile = user.profile

    # NEW: get existing address (may be None)
    address = profile.address

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=address)

        if form.is_valid() and address_form.is_valid():
            address = address_form.save()
            profile = form.save(commit=False)
            profile.address = address
            profile.save()

            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
        address_form = AddressForm(instance=address)

    context = {
        'form': form,
        'address_form': address_form,   # ← ADD THIS
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


def registration_pending_view(request):
    """View shown after registration pending approval."""
    return render(request, 'accounts/registration_pending.html')
