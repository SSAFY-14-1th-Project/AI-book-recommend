from rest_framework import serializers
from .models import Book, BookRating

class BookBestRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('cover', 'title', 'author', 'description')


class BookReviewRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('cover', 'title', 'author')


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = '__all__'