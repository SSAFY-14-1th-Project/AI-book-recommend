<template>
  <!-- ==================== 추천 도서 목록 ==================== -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div
      v-for="(recommendation, index) in recommendations"
      :key="recommendation.id || index"
      class="card bg-base-100 shadow-xl border border-base-content/5 hover:shadow-2xl transition-all duration-300 hover:scale-105 cursor-pointer"
      @click="$emit('book-click', recommendation.id)"
    >
      <figure class="px-6 pt-6">
        <img
          :src="recommendation.cover || '/placeholder-book.png'"
          :alt="recommendation.title"
          class="rounded-lg h-64 w-full object-cover shadow-md"
          @error="(e) => (e.target.src = '/placeholder-book.png')"
        />
      </figure>
      <div class="card-body">
        <!-- 순위 뱃지 -->
        <div class="flex items-center justify-between mb-2">
          <div class="badge badge-primary badge-lg">추천 {{ index + 1 }}위</div>
          <div v-if="recommendation.category" class="badge badge-outline badge-sm">
            {{ recommendation.category }}
          </div>
        </div>

        <!-- 도서 정보 -->
        <h3 class="card-title text-lg line-clamp-2 leading-tight">
          {{ recommendation.title }}
        </h3>
        <p class="text-sm text-base-content/70">
          {{ recommendation.author }}
        </p>

        <!-- 할아버지의 추천 이유 (초기에는 숨김) -->
        <div class="divider my-2"></div>

        <div class="collapse collapse-arrow bg-base-200/50" @click.stop="">
          <input type="checkbox" />
          <div class="collapse-title text-sm font-medium">👴 할아버지가 추천하는 이유</div>
          <div class="collapse-content">
            <p class="text-sm text-base-content/80 leading-relaxed whitespace-pre-wrap">
              {{ recommendation.description || '이 책은 자네에게 딱 맞을 것 같아서 골랐네.' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props & Emits ====================
defineProps({
  recommendations: {
    type: Array,
    required: true,
  },
})

defineEmits(['book-click'])
</script>
