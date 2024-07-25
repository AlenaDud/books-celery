from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer, UserSerializer, RegisterSerializer
from .tasks import upload_books
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication

User = get_user_model()


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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
        category = self.request.query_params.get('category')
        if category:
            try:
                queryset = queryset.filter(category__slug=category)
            except Category.DoesNotExist:
                queryset = queryset.none()
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        serializer = BookSerializer(data=request.data, many=True)
        if serializer.is_valid():
            books_data = serializer.validated_data
            id_categories = [{'id': [category.id for category in book.pop('category')]} for book in books_data]
            upload_books.delay(request.user.id, books_data, id_categories)
            return Response({"status": "Books are being processed"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
