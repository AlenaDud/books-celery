from rest_framework.routers import DefaultRouter
from home.views import BookViewSet, CategoryViewSet
router = DefaultRouter()


router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)