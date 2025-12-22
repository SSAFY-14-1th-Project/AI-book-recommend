from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import BookSerializer, BookDetailSerializer
from .models import Book, Bookmark

# Create your views here.


@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        # 1. best_rank가 null인 데이터를 제외하고 (순위가 있는 것만)
        # 2. best_rank 기준 오름차순 정렬 (1, 2, 3...)
        # 3. 상위 10개만 슬라이싱
        queryset = Book.objects.filter(best_rank__isnull=False).order_by('best_rank')[:10]
        # 데이터가 없으면 자동으로 404를 일으키고, 있으면 리스트를 반환
        books = get_list_or_404(queryset)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'GET':
        serializer = BookDetailSerializer(book, context={'request': request})
        # print(serializer.data)
        return Response(serializer.data)


# 테스트 방법 : /api/v1/books/1/bookmarks/ 에서 Header에 직접
# Authorization을 하고 POST 요청을 보내면 됨
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 로그인한 사용자만 가능
def book_mark(request, id):
    book = get_object_or_404(Book, pk=id)
    user = request.user

    # 현재 사용자가 이 책을 북마크했는지 확인
    bookmark = Bookmark.objects.filter(user=user, book=book)

    if bookmark.exists():
        # 이미 있다면 삭제 (북마크 해제)
        bookmark.delete()
        return Response({'is_bookmarked': False, 'message': '북마크가 해제되었습니다.'})
    else:
        # 없다면 생성 (북마크 등록)
        Bookmark.objects.create(user=user, book=book)
        return Response({'is_bookmarked': True, 'message': '북마크가 등록되었습니다.'})


# @api_view(['GET'])
# def book_bestseller_list(request):



