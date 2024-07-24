from rest_framework import serializers
from .models import Book, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=True
    )

    def create(self, validated_data):
        categories = validated_data.pop('category')
        book = Book.objects.create(**validated_data, user=self.context['request'].user)
        book.category.set(categories)
        return book

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'photo', 'description', 'rating', 'category',]
