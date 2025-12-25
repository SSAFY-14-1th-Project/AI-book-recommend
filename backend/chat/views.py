from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from trades.models import Trade


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enter_chat(request):
    trade_id = request.data.get("trade_id")
    trade = get_object_or_404(Trade, id=trade_id)

    # 판매자는 enter API 호출 못 하게만 막음
    if trade.user_id == request.user.id:
        return Response(
            {"error": "판매자는 채팅을 시작할 수 없습니다."},
            status=400
        )

    # ✅ buyer 저장 안 함
    return Response({
        "trade_id": trade.id
    })
