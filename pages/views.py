from contextlib import contextmanager
from blog.models import Post
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ContactForm
from django.contrib import messages



def home_view(request):
    latest_posts = Post.objects.filter(is_featured=True).order_by('-created_at')
    context = {
        'latest_posts': latest_posts,
        'title': 'Home',
    }
    return render(request, 'pages/index.html', context)


def about_view(request):
    context = {
        'title': 'About Us',
    }
    return render(request, 'pages/about.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully. Thank you!')
            return redirect('pages:contact')

        else:
            messages.error(request, 'Your message could not be sent. Please correct the errors below.')

    else:
        form = ContactForm()
    context = {
        'form': form,
        'title': 'Contact Us',
    }
    return render(request, 'pages/contact.html', context)
