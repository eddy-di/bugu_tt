from django.conf import settings
from django.db import models

from accounts.models import User


class Article(models.Model):
    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'

    VISIBILITY_CHOICES = [
        (PRIVATE, 'Private type article'),
        (PUBLIC, 'Public type article'),
    ]

    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default=PUBLIC)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
