<template>
  <!-- ==================== 거래 도서 정보 카드 ==================== -->
  <div
    class="card bg-base-200/50 shadow-sm border border-base-content/5 hover:shadow-md transition-shadow"
  >
    <div class="card-body p-6">
      <h3 class="text-xl font-bold border-b border-base-content/10 pb-3 mb-4">거래 도서 정보</h3>

      <div class="flex gap-4">
        <!-- 도서 이미지 -->
        <div class="shrink-0">
          <img
            :src="book.cover || '/placeholder-book.png'"
            :alt="book.title"
            class="w-24 h-32 object-cover rounded-lg shadow-sm"
            @error="handleImageError"
          />
        </div>

        <!-- 도서 정보 -->
        <div class="flex-1 flex flex-col justify-between">
          <div class="space-y-2">
            <h4 class="font-bold text-lg line-clamp-2 leading-tight">
              {{ book.title || '제목 없음' }}
            </h4>

            <div class="flex flex-wrap gap-2 items-center">
              <span v-if="book.category" class="badge badge-primary badge-sm">
                {{ book.category?.name }}
              </span>
              <span v-if="book.adult" class="badge badge-warning badge-sm"> 19세 이상 </span>
            </div>

            <div v-if="book.price_standard" class="text-sm text-base-content/70">
              정가: <span class="font-semibold">{{ book.price_standard?.toLocaleString() }}원</span>
            </div>
          </div>

          <!-- 도서 상세보기 버튼 -->
          <div class="mt-3">
            <RouterLink
              :to="{ name: 'bookDetail', params: { id: book.id } }"
              class="btn btn-primary btn-sm btn-outline w-full"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
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
              도서 상세정보 보기
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

// ==================== Props ====================
defineProps({
  book: {
    type: Object,
    required: true,
    default: () => ({}),
  },
})

// ==================== Methods ====================
const handleImageError = (event) => {
  event.target.src = '/placeholder-book.png'
}
</script>
