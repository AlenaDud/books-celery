from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer
from .tasks import upload_books

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            try:
                queryset = queryset.filter(category__slug=category)
            except Category.DoesNotExist:
                queryset = queryset.none()
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        serializer = BookSerializer(data=request.data, many=True)
        if serializer.is_valid():
            upload_books.delay(request.user.id, serializer.validated_data)
            return Response({"status": "Books are being processed"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer