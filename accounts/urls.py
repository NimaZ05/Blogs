from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'


urlpatterns = [
    path('', auth_page, name='auth'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_page, name='profile'),
    path('profile/edit', profile_edit, name='profile_edit'),

    path('user/<slug:slug>/', user_profile_view, name='user_profile'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name='accounts/password_reset_email.html',
            success_url=reverse_lazy('accounts:password_reset_done'),
        ),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url=reverse_lazy('accounts:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'
    ),
]
