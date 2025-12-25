<template>
  <!-- ==================== 도서 그리드 영역 ==================== -->
  <div>
    <!-- 로딩 중 스켈레톤 UI -->
    <div
      v-if="loading"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6"
    >
      <BookCardSkeleton v-for="i in skeletonCount" :key="i" />
    </div>

    <!-- 도서 목록 -->
    <div
      v-else-if="books.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6"
    >
      <BookCard v-for="book in books" :key="book.id" :book="book" />
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
          d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
        />
      </svg>
      <h3 class="text-2xl font-bold text-base-content/50 mb-2">검색 결과가 없습니다</h3>
      <p class="text-base-content/40">다른 검색어나 필터를 사용해보세요</p>
    </div>
  </div>
</template>

<script setup>
import BookCard from '@/components/BookCard.vue'
import BookCardSkeleton from '@/components/BookCardSkeleton.vue'

// ==================== Props ====================
defineProps({
  books: {
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
