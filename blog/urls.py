from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('post/<slug:slug>/', post_view, name='post_detail'), # /post/<slug:slug>
]