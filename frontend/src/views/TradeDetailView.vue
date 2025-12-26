<template>
  <div class="container mx-auto p-4 max-w-4xl" v-if="trade">
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <!-- 상단: 이미지 + 정보 -->
        <div class="flex flex-col md:flex-row gap-6">
          <!-- 상품 이미지 -->
          <div class="flex-shrink-0">
            <img 
              :src="trade.image || '/placeholder.png'" 
              alt="상품 이미지" 
              class="w-full md:w-80 h-80 object-cover rounded-lg"
            />
          </div>

          <!-- 상품 정보 -->
          <div class="flex-1 space-y-4">
            <!-- 거래 상태 배지 -->
            <div class="flex items-center gap-2">
              <span 
                class="badge badge-lg"
                :class="{
                  'badge-success': trade.status === 'available',
                  'badge-warning': trade.status === 'reserved',
                  'badge-neutral': trade.status === 'sold'
                }"
              >
                {{ statusLabel }}
              </span>
              <span class="badge badge-outline">{{ saleTypeLabel }}</span>
            </div>

            <!-- 제목 -->
            <h1 class="text-2xl font-bold">{{ trade.title }}</h1>

            <!-- 가격 -->
            <p class="text-3xl font-bold text-primary">
              {{ trade.saleType === 'free' ? '무료나눔' : `${trade.price.toLocaleString()}원` }}
            </p>

            <!-- 판매자 정보 -->
            <div class="flex items-center gap-2 text-gray-500">
              <span class="font-medium">{{ trade.user.nickname }}</span>
              <span>·</span>
              <span>{{ regionLabel }}</span>
            </div>

            <!-- 조회수 / 작성일 -->
            <div class="text-sm text-gray-400">
              조회 {{ trade.viewCount }} · {{ formatDate(trade.createdAt) }}
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- 상품 설명 -->
        <div class="space-y-2">
          <h2 class="text-lg font-semibold">상품 설명</h2>
          <p class="whitespace-pre-wrap text-gray-600">{{ trade.content }}</p>
        </div>

        <div class="divider"></div>

        <!-- 도서 정보 -->
        <div class="space-y-2">
          <h2 class="text-lg font-semibold">거래 도서</h2>
          <div class="flex items-center gap-4 p-4 bg-base-200 rounded-lg">
            <img 
              :src="trade.book.cover || '/book-placeholder.png'" 
              alt="도서 표지"
              class="w-16 h-20 object-cover rounded"
            />
            <div>
              <p class="font-medium">{{ trade.book.title }}</p>
              <p class="text-sm text-gray-500">{{ trade.book.author }}</p>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- 버튼 영역 -->
        <div class="flex gap-2">
          <!-- 채팅하기 버튼 (본인 아닐 때) -->
          <a
            v-if="trade.kakaoChatUrl && trade.status !== 'sold'"
            :href="trade.kakaoChatUrl"
            target="_blank"
            class="btn btn-primary flex-1"
          >
            채팅하기
          </a>

          <!-- 본인 게시글일 때 -->
          <template v-if="isOwner">
            <button @click="editTrade" class="btn btn-outline flex-1">수정</button>
            <button @click="deleteTrade" class="btn btn-error btn-outline">삭제</button>
          </template>

          <!-- 목록으로 -->
          <button @click="router.push({ name: 'trade-list' })" class="btn btn-ghost">
            목록
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 로딩 -->
  <div v-else class="flex justify-center items-center h-64">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
</template>


<script setup>
// 상태 라벨
const statusLabel = computed(() => {
  const labels = { available: '판매중', reserved: '예약중', sold: '판매완료' }
  return labels[trade.value?.status] || ''
})

// 판매 유형 라벨
const saleTypeLabel = computed(() => {
  return trade.value?.saleType === 'free' ? '무료나눔' : '판매'
})

// 지역 라벨
const regionLabel = computed(() => {
  const regions = {
    all: '전국', seoul: '서울', busan: '부산', daegu: '대구',
    incheon: '인천', gwangju: '광주', daejeon: '대전', ulsan: '울산',
    sejong: '세종', gyeonggi: '경기', gangwon: '강원', chungbuk: '충북',
    chungnam: '충남', jeonbuk: '전북', jeonnam: '전남', gyeongbuk: '경북',
    gyeongnam: '경남', jeju: '제주'
  }
  return regions[trade.value?.region] || ''
})

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ko-KR')
}

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