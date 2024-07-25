from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='book_photos/', null=True, blank=True)
    description = models.TextField()
    rating = models.PositiveIntegerField()
    category = models.ManyToManyField(Category, related_name='books')
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating']
        indexes = [
            models.Index(fields=['title']),
        ]
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/books/" + str(self.title)