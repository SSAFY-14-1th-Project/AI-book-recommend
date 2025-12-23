from django.urls import path
from .views import TradeDetailView, TradeSearchAPIView
from . import views
app_name = 'trades'

urlpatterns = [
    path('search/', TradeSearchAPIView.as_view(), name='search'),
    # 목록 조회
    path('', views.trade_list, name='trade_list'),
    # 게시글 생성 (book_pk 기반)
    path('create/<int:book_pk>/', views.trade_create, name='trade_create'),
    # 게시글 상세, 수정, 삭제: /api/trades/<id>/
    path('<int:trade_id>/', TradeDetailView.as_view(), name='trade_detail'),
]
