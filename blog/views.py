from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F


def paginate_posts(request, post_list, per_page=3):
    """Handles common pagination logic."""
    paginator = Paginator(post_list, per_page)
    try:
        page_number = request.GET.get('page')
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def get_common_context():
    """Returns categories and tags for the sidebar."""
    return {
        'categories': Category.objects.all().only('id', 'name', 'slug').order_by('name'),
        'tags': Tag.objects.all().only('id', 'name', 'slug').order_by('name'),
    }


def blog_home(request):
    posts = Post.objects.filter(status="published") \
        .select_related('category', 'author') \
        .prefetch_related('tags') \
        .order_by('-published_date')

    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'title': 'Blog',
    })
    return render(request, 'blog/blog.html', context)


def post_view(request, slug):
    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'author').prefetch_related('tags'),
        slug=slug,
        status="published"
    )

    session_key = f'viewed_post_{post.pk}'
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(counted_view=F('counted_view') + 1)
        request.session[session_key] = True
        post.refresh_from_db()

    related_posts = Post.objects.filter(
        category=post.category,
        status="published"
    ).exclude(pk=post.pk).order_by('?')[:2]

    context = {
        'post': post,
        'title': post.title,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post.html', context)


def blog_search(request):
    posts = Post.objects.filter(status="published")
    search_query = request.GET.get('search', '').strip()

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(
                content__icontains=search_query)
        )

    posts = posts.order_by('-published_date')
    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'search_query': search_query,
        'title': f'Search: {search_query}' if search_query else 'Search Results',
    })

    return render(request, 'blog/blog.html', context)


def blog_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Post.objects.filter(
        category=category,
        status="published"  # Consistency fix: use "published" string
    ).select_related('category', 'author').prefetch_related('tags').order_by('-published_date')

    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'filter_type': 'category',
        'filter_slug': cat_slug,  # Used for pagination links
        'title': f'Category: {category.name}',
    })
    return render(request, 'blog/blog.html', context)


def blog_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(
        tags=tag,
        status="published"
    ).select_related('category', 'author').prefetch_related('tags').order_by('-published_date')

    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'filter_type': 'tag',
        'filter_slug': tag_slug,
        'title': f'Tag: {tag.name}',
    })
    return render(request, 'blog/blog.html', context)


def blog_author(request, author_username):
    posts = Post.objects.filter(
        author__username=author_username,
        status="published"
    ).select_related('category', 'author').prefetch_related('tags').order_by('-published_date')

    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'filter_type': 'author',
        'filter_slug': author_username,
        'title': f'Author: {author_username}',
    })
    return render(request, 'blog/blog.html', context)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form.save_m2m()
            messages.success(request, f"Post '{new_post.title}' successfully created!")
            return redirect('blog:post_detail', slug=new_post.slug)
        else:
            messages.error(request, "There was an error in your submission. Please check the fields.")
    else:
        form = PostForm()
    context = get_common_context()
    context.update({
        'form': form,
        'title': 'add post',
    })
    return render(request, 'blog/add_post.html', context)
