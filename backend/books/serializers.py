# books/serializers.py

from rest_framework import serializers
from .models import Book, BookRating, Bookmark, Category

# 책 검색 Serializer
class BookSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "category",
            "adult",
        ]

# 책 평점 Serializer
class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['score', 'user', 'created_at']

# 책 북마크 Serializer
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['user', 'created_at']

# 책 Serializer
class BookSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # ID 값으로 직렬화
    ratings = BookRatingSerializer(many=True, read_only=True)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    bookmark_status = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'isbn', 'publisher', 'pub_date', 'cover', 'description', 'price_sales', 'adult', 'ratings', 'average_rating', 'bookmark_status']

    def get_bookmark_status(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Bookmark.objects.filter(user=user, book=obj).exists()
        return False