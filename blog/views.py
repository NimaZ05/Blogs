from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def blog_home(request, **kwargs):
    posts = Post.objects.filter(status="published")

    if kwargs.get('cat_name') is not None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if kwargs.get('author_username') is not None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') is not None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])

    context = {
        'posts': posts,
        'title': 'Blog',
    }
    return render(request, 'blog/blog.html', context)


def post_view(request, slug,):
    post = get_object_or_404(Post, slug=slug, status="published")

    context = {
        'post': post,
    }
    return render(request, 'blog/post.html', context)
