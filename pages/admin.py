from django.contrib import admin
from .models import *


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject','email', 'phone', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject'),
            'description': 'Submitted Contact Information and Subject',
        }),
        ('Message Content', {
            'fields': ('message',),
            'description': 'The full text of the user\'s inquiry.',
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )