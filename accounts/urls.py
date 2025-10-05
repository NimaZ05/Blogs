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
]
