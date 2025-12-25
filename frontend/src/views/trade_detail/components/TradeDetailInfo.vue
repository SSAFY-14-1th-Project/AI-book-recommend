<template>
  <!-- ==================== 중고거래 상세 정보 ==================== -->
  <div class="flex flex-col gap-8">
    <!-- 도서 정보 -->
    <div class="space-y-4">
      <h3 class="text-xl font-bold border-b border-base-content/10 pb-2">거래 도서 정보</h3>
      <div class="grid grid-cols-1 gap-4">
        <div
          v-if="book.priceStandard"
          class="flex justify-between items-center py-3 border-b border-base-content/5"
        >
          <span class="text-base-content/70">정가</span>
          <span class="font-semibold">{{ book.priceStandard?.toLocaleString() }}원</span>
        </div>
        <div v-if="book.category" class="flex justify-between items-center py-3">
          <span class="text-base-content/70">카테고리</span>
          <span class="badge badge-primary">{{ book.category?.name }}</span>
        </div>
      </div>
    </div>

    <!-- 거래 내용 -->
    <div class="space-y-4">
      <h3 class="text-xl font-bold border-b border-base-content/10 pb-2">거래 설명</h3>
      <div class="prose max-w-none">
        <p class="text-base-content/80 whitespace-pre-wrap leading-relaxed">
          {{ content || '상세 설명이 없습니다.' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props ====================
defineProps({
  book: {
    type: Object,
    default: () => ({}),
  },
  content: {
    type: String,
    default: '',
  },
})
</script>
