from rest_framework import serializers
from accounts.serializers import UserSimpleSerializer  # 이미 만들어진 UserSerializer
from books.serializers import BookTradeSerializer # 도서 요약 정보용
from .models import Trade, Book
import re

class TradeSearchSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_adult = serializers.CharField(source='book.adult', read_only=True)
    book_price_standard = serializers.IntegerField(source='book.price_standard', read_only=True)
    seller = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Trade
        fields = [
            'id',
            'title',
            'content',
            'sale_type',
            'price',
            'region',
            'status',
            'book_title',
            'book_adult',
            'book_price_standard',
            'seller',
            'image',
            'created_at',
        ]

class TradeSerializer(serializers.ModelSerializer):
    """게시글 등록 및 목록 조회용"""
    # 판매자 정보는 읽기 전용으로 (서버에서 request.user로 넣어줄 예정)
    # 중첩 필드는 여기서 얌전히 있자 ㅇㅇ
    
    # user = UserSerializer(read_only=True)
    # user -> id, nickname => UserSimpleSerializer 추가
    user = UserSimpleSerializer(read_only=True)
    
    # book -> adult, title, price_standard, category 추가
    # book = BookTradeSerializer(read_only=True)

    book = BookTradeSerializer(read_only=True)

    # 생성할 때만 받고, 응답에는 포함 안 함
    kakao_chat_url = serializers.CharField(write_only=True, required=False, allow_blank=True)
    def validate_kakao_chat_url(self, value):
        """카카오톡 오픈채팅 URL 형식 검증"""
        if value:
            pattern = r'^https://open\.kakao\.com/o/[a-zA-Z0-9]+$'
            if not re.match(pattern, value):
                raise serializers.ValidationError(
                    "올바른 카카오톡 오픈채팅 URL 형식이 아닙니다."
                )
        return value
    
    class Meta:
        model = Trade
        # 메인 페이지는 content, kakao_chat_url 필요 없음
        fields = [
            'id', 'user', 'book', 'title', 'content',
            'sale_type', 'price', 'region', 'status', 
            'image', 'view_count', 'created_at', 'kakao_chat_url'
        ]
        # 클라이언트(Vue/Postman)가 보내는 데이터에서는 이 필드들을 무시하고, 서버가 주는 데이터(응답)에만 포함해라
        # 조회수 : POST로 주작 가능
        read_only_fields = ['view_count', 'created_at', 'updated_at']

        def validate_kakao_chat_url(self, value):
            """카카오톡 오픈채팅 URL 형식 검증"""
            if value:
                pattern = r'^https://open\.kakao\.com/o/[a-zA-Z0-9]+$'
                if not re.match(pattern, value):
                    raise serializers.ValidationError(
                        "올바른 카카오톡 오픈채팅 URL 형식이 아닙니다. (예: https://open.kakao.com/o/abc123)"
                    )
            return value
    
        def to_representation(self, instance):
            """응답 데이터 커스터마이징 - 본인 게시글이면 카카오 URL 숨기기"""
            data = super().to_representation(instance)
            request = self.context.get('request')

            # 본인 게시글이면 kakao_chat_url 제거
            if request and request.user.is_authenticated:
                if request.user == instance.user:
                    data.pop('kakao_chat_url', None)

            return data


class TradeDetailSerializer(serializers.ModelSerializer):
    """게시글 단일 조회(상세 페이지)용"""
    # user = UserSerializer(read_only=True)
    # user id, nickname만 뻬오기 => UserSimpleSerializer 추가
    user = UserSimpleSerializer(read_only=True)

    # 책 정보도 단순 ID가 아니라 제목, 커버 등이 보이게 중첩 시리얼라이저 사용
    # book -> price_standard, adult, title, category
    book = BookTradeSerializer(read_only=True)
    
    class Meta:
        model = Trade
        # fields = '__all__' # 모든 필드 포함
        fields = [
            'id', 'user', 'book', 'title', 'content', 
            'sale_type', 'price', 'region', 'status', 
            'image', 'kakao_chat_url', 'view_count', 
            'created_at', 'updated_at'
        ]
        # [중요] 상세 페이지에서도 조작 방지를 위해 반드시 추가해야 함! - 회고록에 쓸거 생겼노 ㅎ
        read_only_fields = ['view_count', 'created_at', 'updated_at']


# 중고거래 요약용 serializer
class TradePreviewSerializer(serializers.ModelSerializer):
    # seller = serializers.CharField(source='user.nickname', read_only=True)
    seller = serializers.SerializerMethodField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_price_standard = serializers.IntegerField(source='book.price_standard', read_only=True)

    def get_seller(self, obj):
        return obj.user.nickname

    class Meta:
        model = Trade
        fields = [
            'id',
            'title',
            'book_title',
            'price',
            'sale_type',
            'status',
            'region',
            'seller',
            'image',
            'book_price_standard',
            'created_at',
        ]
