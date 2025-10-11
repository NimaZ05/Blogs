from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


# --- Helper function for pagination, used by all list views ---
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


# --- Common context function ---
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

    # Apply pagination
    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'title': 'Blog',
    })
    return render(request, 'blog/blog.html', context)


def post_view(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author').prefetch_related('tags'),
        slug=slug,
        status="published"
    )

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
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    # Apply ordering and pagination
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


# --- New Views for Tag and Author filtering for cleaner URL structure ---

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
    # Assuming your Post model's author is linked to Django's default User model
    # and we filter by username directly.
    posts = Post.objects.filter(
        author__username=author_username,
        status="published"
    ).select_related('category', 'author').prefetch_related('tags').order_by('-published_date')

    # If no posts are found, we might want to check if the author exists, but for brevity,
    # we'll just show an empty page if the username is valid but has no published posts.

    posts = paginate_posts(request, posts)

    context = get_common_context()
    context.update({
        'posts': posts,
        'filter_type': 'author',
        'filter_slug': author_username,
        'title': f'Author: {author_username}',
    })
    return render(request, 'blog/blog.html', context)
