from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       UserChangeForm)
from .models import Profile

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='username',
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username or Email',
            }
        )
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field},
                )

            if not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

        return self.cleaned_data  # Must return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}  # <-- This will now work
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password'}  # <-- This will now work
        )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('job_title', 'location', 'website', 'bio', 'website', 'image')
