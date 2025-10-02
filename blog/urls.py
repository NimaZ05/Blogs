from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogPageView.as_view(), name='blog'),
    path('<post>', PostPageView.as_view(), name='post'), # /post/<slug:slug>
]