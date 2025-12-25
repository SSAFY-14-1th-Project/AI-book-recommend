from django.db import models
from django.conf import settings
from trades.models import Trade

User = settings.AUTH_USER_MODEL


class ChatRoom(models.Model):
    trade = models.ForeignKey(
        Trade,
        on_delete=models.CASCADE,
        related_name="chat_rooms"
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="seller_chat_rooms"
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_chat_rooms"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trade", "buyer")

    def __str__(self):
        return f"ChatRoom {self.id} (trade={self.trade_id})"


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} (room={self.room_id})"
