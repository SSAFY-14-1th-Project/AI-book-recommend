<template>
  <div class="trade-list container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">중고거래</h1>
      <router-link :to="{ name: 'trade-create' }" class="btn btn-primary">
        글쓰기
      </router-link>
    </div>

    <!-- 거래 목록 -->
    <div v-if="trades.length > 0" class="grid gap-4">
      <div
        v-for="trade in trades"
        :key="trade.id"
        class="card card-side bg-base-100 shadow-md cursor-pointer hover:shadow-lg transition-shadow"
        @click="goToDetail(trade.id)"
      >
        <!-- 이미지 -->
        <figure class="w-32 h-32 flex-shrink-0">
          <img
            :src="trade.image ? `http://localhost:8000${trade.image}` : '/placeholder.png'"
            :alt="trade.title"
            class="w-full h-full object-cover"
          />
        </figure>

        <!-- 정보 -->
        <div class="card-body p-4">
          <h2 class="card-title text-lg">{{ trade.title }}</h2>
          <p class="text-sm text-gray-500">{{ trade.region }} · {{ formatDate(trade.createdAt) }}</p>
          <p class="font-bold text-lg">
            {{ trade.saleType === 'free' ? '무료나눔' : `${trade.price?.toLocaleString()}원` }}
          </p>
          <div class="flex gap-2">
            <span class="badge" :class="getStatusBadgeClass(trade.status)">
              {{ getStatusText(trade.status) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 빈 목록 -->
    <div v-else class="text-center py-12 text-gray-500">
      <p>등록된 거래가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTradeList } from '@/api/trades'

const router = useRouter()
const trades = ref([])

onMounted(async () => {
  try {
    const response = await getTradeList()
    trades.value = response.data
  } catch (error) {
    console.error('거래 목록 조회 실패:', error)
  }
})

const goToDetail = (id) => {
  router.push({ name: 'trade-detail', params: { id } })
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '오늘'
  if (days === 1) return '어제'
  if (days < 7) return `${days}일 전`
  return date.toLocaleDateString('ko-KR')
}

const getStatusText = (status) => {
  const statusMap = {
    available: '판매중',
    reserved: '예약중',
    sold: '판매완료'
  }
  return statusMap[status] || status
}

const getStatusBadgeClass = (status) => {
  const classMap = {
    available: 'badge-success',
    reserved: 'badge-warning',
    sold: 'badge-ghost'
  }
  return classMap[status] || ''
}
</script>
