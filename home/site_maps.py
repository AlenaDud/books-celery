from django.contrib.sitemaps import GenericSitemap


from .models import Book, Category

sitemaps = {
    'books': GenericSitemap({
        'queryset': Book.objects.all(),
        'date_field': 'created_at',
    }),
}
