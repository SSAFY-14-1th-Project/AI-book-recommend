# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # 1️⃣ URL에서 trade_id 가져오기
            self.trade_id = self.scope["url_route"]["kwargs"]["room_id"]
            self.user = self.scope["user"]

            # # 2️⃣ 로그인 안 했으면 차단
            # if self.user.is_anonymous:
            #     await self.close()
            #     return

            # 3️⃣ Trade 조회 (models import는 함수 안에서)
            trade = await self.get_trade(self.trade_id)
            if not trade:
                await self.close()
                return

            seller_id = trade.user_id

            # 4️⃣ 핵심 조건
            # - 판매자는 항상 허용
            # - 구매자는 "채팅하기 눌렀을 때"만 접속하도록 프론트에서 제어
            # (Consumer에서는 판매자 + 한 명만 허용한다고 가정)
            if self.user.id != seller_id:
                # 판매자가 아니면 "구매자 1명"으로 취급
                # 👉 여기서 추가 제한을 더 두고 싶으면 이 자리에 조건 추가
                pass

            # 5️⃣ 그룹 이름 (기존 단체 채팅 구조 유지)
            self.room_group_name = f"trade_{self.trade_id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print("✅ WebSocket CONNECT:", self.user, self.room_group_name)

        except Exception as e:
            print("❌ CONNECT ERROR:", e)
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        # 6️⃣ 같은 방(trade)에 있는 사람들에게만 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    # ================= DB =================

    @database_sync_to_async
    def get_trade(self, trade_id):
        from trades.models import Trade
        try:
            return Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return None
