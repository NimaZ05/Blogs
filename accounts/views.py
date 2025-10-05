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
