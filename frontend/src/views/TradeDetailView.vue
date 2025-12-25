<template>
  <div class="trade-detail" v-if="trade">
    <!-- 상품 이미지 -->
    <div class="trade-image">
      <img :src="trade.image" alt="상품 이미지" />
    </div>

    <!-- 판매자 정보 -->
    <div class="seller-info">
      <span>{{ trade.user.nickname }}</span>
      <span>{{ trade.region }}</span>
    </div>

    <!-- 상품 정보 -->
    <div class="trade-info">
      <h1>{{ trade.title }}</h1>
      <p class="price">{{ trade.price.toLocaleString() }}원</p>
      <p class="status">{{ trade.status }}</p>
      <p class="content">{{ trade.content }}</p>
    </div>

    <!-- 도서 정보 -->
    <div class="book-info">
      <h3>거래 도서</h3>
      <p>{{ trade.book.title }}</p>
      <p>{{ trade.book.author }}</p>
    </div>

    <!-- 채팅하기 버튼 -->
    <!-- 백엔드에서 본인 게시글이면 kakaoChatUrl이 null로 옴 -->
    <a
      v-if="trade.kakaoChatUrl"
      :href="trade.kakaoChatUrl"
      target="_blank"
      class="btn btn-primary chat-btn"
    >
      💬 채팅하기
    </a>

    <!-- 본인 게시글일 때 수정/삭제 버튼 -->
    <div v-if="isOwner" class="owner-actions">
      <button @click="editTrade" class="btn">수정</button>
      <button @click="deleteTrade" class="btn btn-danger">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/loginStore'
import { getTradeDetail, deleteTrade as deleteTradeApi } from '@/api/trades'

const route = useRoute()
const router = useRouter()
const loginStore = useLoginStore()

const trade = ref(null)

// 본인 게시글 여부 확인
const isOwner = computed(() => {
  if (!trade.value || !loginStore.user) return false
  return trade.value.user.id === loginStore.user.id
})

onMounted(async () => {
  const { id } = route.params
  const response = await getTradeDetail(id)
  trade.value = response.data
})

const editTrade = () => {
  router.push({ name: 'trade-edit', params: { id: trade.value.id } })
}

const deleteTrade = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await deleteTradeApi(trade.value.id)
    router.push({ name: 'trade-list' })
  }
}
</script>