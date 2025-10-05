from contextlib import contextmanager
from blog.models import Post
from django.shortcuts import render
from django.views.generic import TemplateView


def home_view(request):
    latest_posts = Post.objects.order_by('-published_date')[:3]
    context = {
        'latest_posts':latest_posts,
        'title': 'Home',
    }
    return render(request, 'pages/index.html', context)


def about_view(request):
    context = {
        'title': 'About Us',
    }
    return render(request, 'pages/about.html', context)


def contact_view(request):
    context = {
        'title': 'Contact Us',
    }
    return render(request, 'pages/contact.html', context)
