import profile

from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', auth_page, name='auth'),
    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('profile', profile_page, name='profile'),
    path('password_reset/', forgot_password_view, name='password_reset'),
    path('change_password/', change_password_view, name='change_password'),
    path('delete_account/', delete_account_view, name='delete_account'), # <int:pk>/
]
