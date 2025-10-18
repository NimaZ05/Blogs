from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name='Full Name')
    email = models.EmailField(db_index=True)
    phone = PhoneNumberField(max_length=20, blank=True, null=True)
    message = models.TextField()
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.subject[:50]} ...'


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    unsubscribe_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-signup_date']

    def __str__(self):
        return self.email
