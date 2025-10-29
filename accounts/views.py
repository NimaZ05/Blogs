from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Profile
from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

SUCCESS_REDIRECT_URL = 'accounts:profile'
CUSTOM_BACKEND_PATH = 'accounts.backends.EmailOrUsernameModelBackend'


def auth_page(request):
    context = {
        'title': 'Registration'
    }
    return render(request, 'accounts/auth.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(SUCCESS_REDIRECT_URL)

    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! You are now logged in.')
                return redirect(SUCCESS_REDIRECT_URL)
    else:
        form = CustomAuthenticationForm()

    context = {
        'login_form': form,
        'title': 'Login',
    }
    return render(request, 'accounts/login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect(SUCCESS_REDIRECT_URL)
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user, CUSTOM_BACKEND_PATH)
            messages.success(request, f'Welcome to our site, {user.username}! You are now logged in.')
            return redirect(SUCCESS_REDIRECT_URL)

    context = {
        'signup_form': form,
        'title': 'Signup'
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        messages.success(request, 'logged out successfully')
        logout(request)
        return redirect('/')
    context = {
        'title': 'Logout'
    }
    return render(request, 'accounts/logout_confirm.html', context)


def profile_page(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'title': f'{request.user.username}\'s Profile Management',
        'profile_data': profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'title': f'{request.user.username}\'s Profile Management',
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/profile_edit.html', context)


def user_profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user
    context = {
        'title': f'{user.username}\'s Profile',
        'user_data': user,
        'profile_data': profile,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        if user.check_password(password):
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('/')
        else:
            messages.error(request, 'Your password does not match.')
            return render(request, 'accounts/delete_account.html', {'title': 'Delete Account'})

    context = {
        'title': 'Delete Account'
    }
    return render(request, 'accounts/delete_account.html', context)
