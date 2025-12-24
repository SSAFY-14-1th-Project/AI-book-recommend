# chats/models.py
from django.db import models
from django.conf import settings
from trades.models import Trade

User = settings.AUTH_USER_MODEL

class ChatRoom(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_rooms')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trade', 'buyer')


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

