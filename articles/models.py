from django.conf import settings
from django.db import models

from accounts.models import User


class Article(models.Model):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=DRAFT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
