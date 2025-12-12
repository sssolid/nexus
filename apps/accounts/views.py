"""
Views for the accounts application.
"""
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import User, UserProfile

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)

def async_send(func, *args, **kwargs):
    executor.submit(func, *args, **kwargs)


class CustomLoginView(LoginView):
    """Custom login view with email-based authentication."""
    
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect based on user type."""
        user = self.request.user
        if user.is_employee:
            return reverse_lazy('products:product_list')
        return reverse_lazy('products:customer_catalog')


class UserRegistrationView(CreateView):
    """View for customer registration."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:registration_pending')

    def form_valid(self, form):
        """Handle registration and notify admin."""
        response = super().form_valid(form)

        # Extract newly created user object
        user = self.object

        # Send email notification
        async_send(self.send_registration_notification, user)

        return response

    def send_registration_notification(self, user):
        subject = f"New User Registration: {user.email}"
        text_body = (
            f"A new customer has registered.\n\n"
            f"Name: {user.get_full_name()}\n"
            f"Email: {user.email}\n"
            f"Username: {user.username}\n"
        )
        html_body = f"""
        <h2>New User Registration</h2>
        <p><strong>Name:</strong> {user.get_full_name()}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Username:</strong> {user.username}</p>
        """

        msg = EmailMultiAlternatives(
            subject,
            text_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.SUPPORT_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()


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


# Error handlers
def error_400(request, exception=None):
    """Handle 400 Bad Request errors."""
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception=None):
    """Handle 403 Forbidden errors."""
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception=None):
    """Handle 404 Not Found errors."""
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    """Handle 500 Internal Server errors."""
    return render(request, 'errors/500.html', status=500)
