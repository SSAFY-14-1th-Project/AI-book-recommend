# books/urls.py
from django.urls import path
from .views import BookSearchAPIView, BookDetailAPIView

appname = 'books'
urlpatterns = [
    path('search/', BookSearchAPIView.as_view(), name='search'),
    path('detail/<int:pk>/', BookDetailAPIView.as_view(), name='detail'),
]