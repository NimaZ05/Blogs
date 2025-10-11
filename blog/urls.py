from django.urls import path
# Import new views: blog_tag, blog_author
from .views import blog_home, post_view, blog_search, blog_category, blog_tag, blog_author

app_name = 'blog'

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('post/<slug:slug>/', post_view, name='post_detail'),
    path('search/' , blog_search, name='search'),
    path('category/<slug:cat_slug>/', blog_category, name='category'),
    path('tag/<slug:tag_slug>/', blog_tag, name='tag'),
    path('author/<str:author_username>/', blog_author, name='author'),
]