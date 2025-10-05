from django.contrib import admin
from django.utils.html import format_html

from .models import Post, Category, Tag


# Assuming your models are defined in a file named models.py
# in the same application directory.

# --- 1. Category Admin Configuration ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name',)
    # Automatically generate slug from name
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        """Custom column to display the number of posts in this category."""
        return obj.posts.count()

    post_count.short_description = 'Posts'


# --- 2. Tag Admin Configuration ---

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    # Automatically generate slug from name
    prepopulated_fields = {'slug': ('name',)}


# --- 3. Post Admin Configuration ---

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model (the main model).
    """
    readonly_fields = ('slug',)

    # Display columns in the change list view
    list_display = ('title', 'author', 'status_colored', 'category', 'is_featured', 'published_date', 'created_at')

    # Enable filtering on the sidebar
    list_filter = ('status', 'category', 'author', 'is_featured', 'published_date')

    # Fields to search across
    search_fields = ('title', 'content', 'summary')

    # Automatically generate slug from title (if slug is editable, which it should be)
    # Since the model sets slug editable=False, we will rely on the model's save method for generation.
    # To show it in the admin and ensure it's generated, we keep it in the fieldsets below.

    # Adds a date-based drill-down navigation at the top of the change list
    date_hierarchy = 'published_date'

    # Order the change list view by published date descending (newest first)
    ordering = ('-published_date', '-created_at')

    # Use a faster, pop-up selection widget for ForeignKey fields that might have many records
    raw_id_fields = ('author',)
    autocomplete_fields = ('author',)
    exclude = ('slug',)

    # Organize fields into logical groups in the detail view
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'content'),
        }),
        ('Publication Details', {
            'fields': ('author', 'status', 'published_date', 'is_featured', 'image'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
            'description': 'Assign the primary category and optional tags.',
        }),
        ('SEO & URL Management', {
            # Slug is required, but since we auto-generate it in the model,
            # we make it readonly here to prevent accidental changes after creation.
            'fields': ('slug',),
            'classes': ('collapse',),
            'description': 'The slug is auto-generated upon saving the post title.',
        }),
    )

    # Custom method for coloring the status text
    def status_colored(self, obj):
        """Displays the status with a visual cue based on its value."""
        color = 'gray'
        if obj.status == 'published':
            color = 'green'
        elif obj.status == 'draft':
            color = 'orange'

        return format_html('<span style="color: {}">{}</span>', color, obj.get_status_display())

    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
