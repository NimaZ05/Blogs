from django.urls import path
from .views import *
app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('singup', SignUpView.as_view(), name='signup'),
]