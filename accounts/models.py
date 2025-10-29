from audioop import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics')
    job_title = models.CharField(max_length=100, blank=True, default='No Job')
    location = models.CharField(max_length=100, blank=True, default='No Public Location')
    website = models.URLField(max_length=200, blank=True, null=True, default='No Website')
    bio = models.TextField(max_length=500, blank=True,
                           default="Unfortunately This User Doesn't Want To Share Anything")
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_username = self.user.username if self.user_id else None

    def save(self, *args, **kwargs):
        is_new_user = not self.pk
        username_changed = self.user.username != self.__original_username if self.user_id else False

        if is_new_user or username_changed:
            base_slug = slugify(self.user.username)
            queryset = Profile.objects.all()

            slug_exists = True
            count = 1
            final_slug = base_slug

            while slug_exists:
                if queryset.filter(slug=final_slug).exists():
                    final_slug = f'{base_slug}-{count}'
                    count += 1
                else:
                    self.slug = final_slug
                    slug_exists = False

        super().save(*args, **kwargs)
        self.__original_username = self.user.username

    def get_absolute_url(self):
        return reverse('accounts:user_profile', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.user.username} Profile'
