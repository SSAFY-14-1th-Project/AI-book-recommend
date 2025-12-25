<template>
  <!-- ==================== 중고거래 그리드 영역 ==================== -->
  <div>
    <!-- 로딩 중 스켈레톤 UI -->
    <div
      v-if="loading"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6"
    >
      <TradeCardSkeleton v-for="i in skeletonCount" :key="i" />
    </div>

    <!-- 거래 목록 -->
    <div
      v-else-if="trades.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6"
    >
      <TradeCard v-for="trade in trades" :key="trade.id" :trade="trade" />
    </div>

    <!-- 검색 결과 없음 -->
    <div v-else class="flex flex-col items-center justify-center py-20 text-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-24 w-24 text-base-content/20 mb-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
        />
      </svg>
      <h3 class="text-2xl font-bold text-base-content/50 mb-2">검색 결과가 없습니다</h3>
      <p class="text-base-content/40">다른 검색어나 필터를 사용해보세요</p>
    </div>
  </div>
</template>

<script setup>
import TradeCard from '@/components/TradeCard.vue'
import TradeCardSkeleton from './TradeCardSkeleton.vue'

// ==================== Props ====================
defineProps({
  trades: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  skeletonCount: {
    type: Number,
    default: 20,
  },
})
</script>
