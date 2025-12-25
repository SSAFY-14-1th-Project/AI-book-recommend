<template>
  <!-- ==================== 북마크 도서 목록 ==================== -->
  <div class="card bg-base-100 shadow-lg border border-base-content/10">
    <div class="card-body p-8">
      <h2 class="text-2xl font-bold mb-6">북마크한 도서</h2>

      <!-- 로딩 중 -->
      <div v-if="loading" class="flex justify-center py-12">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- 북마크 목록 -->
      <div v-else-if="props.bookmarks.length > 0" class="space-y-4 h-100 overflow-auto">
        <div
          v-for="book in props.bookmarks"
          :key="book.id"
          class="flex gap-4 p-4 rounded-lg border border-base-content/10 hover:bg-base-200/50 transition-colors cursor-pointer"
          @click="$emit('book-click', book.id)"
        >
          <!-- 도서 이미지 -->
          <img
            :src="book.cover || '/placeholder-book.png'"
            :alt="book.title"
            class="w-20 h-28 object-cover rounded-lg shadow-sm"
            @error="(e) => (e.target.src = '/placeholder-book.png')"
          />

          <!-- 도서 정보 -->
          <div class="flex-1 min-w-0">
            <h3 class="font-bold text-lg line-clamp-2 leading-tight mb-2">
              {{ book.title }}
            </h3>
            <p class="text-sm text-base-content/70 mb-2">{{ book.author }}</p>
          </div>

          <!-- 화살표 아이콘 -->
          <div class="flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-base-content/30"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </div>
        </div>
      </div>

      <!-- 북마크 없음 -->
      <div v-else class="text-center py-12">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-24 w-24 mx-auto text-base-content/20 mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
          />
        </svg>
        <p class="text-base-content/50 mb-4">아직 북마크한 도서가 없습니다</p>
        <RouterLink :to="{ name: 'bookSearch' }" class="btn btn-primary btn-sm">
          도서 둘러보기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

// ==================== Props & Emits ====================
const props = defineProps({
  bookmarks: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['book-click'])
</script>
