# chats/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatRoom
from trades.models import Trade

@api_view(['POST'])
def enter_chat(request):
    trade = Trade.objects.get(id=request.data['trade_id'])

    room, created = ChatRoom.objects.get_or_create(
        trade=trade,
        buyer=request.user,
        defaults={'seller': trade.user}
    )

    return Response({
        'room_id': room.id
    })
