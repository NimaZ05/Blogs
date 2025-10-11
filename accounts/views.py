from django.shortcuts import render
from django.template.defaultfilters import title


def auth_page(request):
    context = {
        'title': 'Registration'
    }
    return render(request, 'accounts/auth.html', context)


def login_view(request):
    context = {
        'title': 'Login'
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    context = {
        'title': 'Logout'
    }
    return render(request, 'accounts/login.html', context)


def signup_view(request):
    context = {
        'title': 'Signup'
    }
    return render(request, 'accounts/signup.html', context)


def profile_page(request):
    context = {
        'title': 'Profile'
    }
    return render(request, 'accounts/profile.html', context)


def forgot_password_view(request):
    context = {
        'title': 'Forgot Password'
    }
    return render(request, 'accounts/password_reset.html', context)


def change_password_view(request):
    context = {
        'title': 'Change Password'
    }
    return render(request, 'accounts/password_change.html', context)


def delete_account_view(request):
    context = {
        'title': 'Delete Account'
    }
    return render(request, 'accounts/delete_account.html', context)
