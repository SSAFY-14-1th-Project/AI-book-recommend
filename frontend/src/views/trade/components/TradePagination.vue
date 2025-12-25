<template>
  <!-- ==================== 페이지네이션 영역 ==================== -->
  <div v-if="totalPages > 1" class="flex justify-center mt-8">
    <div class="join">
      <!-- 이전 페이지 버튼 -->
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="join-item btn btn-sm md:btn-md"
      >
        «
      </button>

      <!-- 페이지 번호 버튼들 -->
      <template v-for="page in displayPages" :key="page">
        <!-- 페이지 번호 -->
        <button
          v-if="page !== '...'"
          @click="goToPage(page)"
          :class="['join-item btn btn-sm md:btn-md', currentPage === page ? 'btn-active' : '']"
        >
          {{ page }}
        </button>
        <!-- 생략 표시 -->
        <button v-else class="join-item btn btn-sm md:btn-md btn-disabled">...</button>
      </template>

      <!-- 다음 페이지 버튼 -->
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="join-item btn btn-sm md:btn-md"
      >
        »
      </button>
    </div>
  </div>

  <!-- 페이지 정보 표시 -->
  <div v-if="totalPages > 0" class="text-center mt-4 text-sm text-base-content/70">
    {{ currentPage }} / {{ totalPages }} 페이지 (총 {{ totalCount }}개)
  </div>
</template>

<script setup>
import { computed } from 'vue'

// ==================== Props & Emits ====================
const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  totalCount: {
    type: Number,
    default: 0,
  },
  maxVisiblePages: {
    type: Number,
    default: 5,
  },
})

const emit = defineEmits(['update:currentPage'])

// ==================== Computed ====================
// 표시할 페이지 번호들 계산
const displayPages = computed(() => {
  const pages = []
  const { currentPage, totalPages, maxVisiblePages } = props

  // 전체 페이지가 maxVisiblePages 이하면 모두 표시
  if (totalPages <= maxVisiblePages) {
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i)
    }
    return pages
  }

  // 항상 첫 페이지 표시
  pages.push(1)

  // 현재 페이지 기준으로 표시할 범위 계산
  const halfVisible = Math.floor((maxVisiblePages - 2) / 2)
  let startPage = Math.max(2, currentPage - halfVisible)
  let endPage = Math.min(totalPages - 1, currentPage + halfVisible)

  // 시작 부분 조정
  if (currentPage - halfVisible < 2) {
    endPage = Math.min(totalPages - 1, maxVisiblePages - 1)
  }

  // 끝 부분 조정
  if (currentPage + halfVisible > totalPages - 1) {
    startPage = Math.max(2, totalPages - maxVisiblePages + 2)
  }

  // 첫 페이지와 시작 페이지 사이에 간격이 있으면 생략 표시
  if (startPage > 2) {
    pages.push('...')
  }

  // 중간 페이지들 추가
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }

  // 끝 페이지와 마지막 페이지 사이에 간격이 있으면 생략 표시
  if (endPage < totalPages - 1) {
    pages.push('...')
  }

  // 항상 마지막 페이지 표시
  if (totalPages > 1) {
    pages.push(totalPages)
  }

  return pages
})

// ==================== Methods ====================
const goToPage = (page) => {
  if (page < 1 || page > props.totalPages || page === props.currentPage) {
    return
  }
  emit('update:currentPage', page)
}
</script>
