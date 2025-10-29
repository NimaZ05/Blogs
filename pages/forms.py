from django import forms
from .models import Contact, NewsletterSubscription
from django.forms.widgets import TextInput, EmailInput, Textarea


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Full Name *',
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Email *',
            }),
            'phone': TextInput(attrs={
                'placeholder': 'Phone',
            }),
            'subject': TextInput(attrs={
                'placeholder': 'Subject *',
            }),
            'message': Textarea(attrs={
                'placeholder': 'Your message here...',
                'rows': 6,
            }),
        }
