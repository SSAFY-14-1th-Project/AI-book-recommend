<template>
  <!-- ==================== 중고거래 이미지 ==================== -->
  <figure class="flex justify-center items-start bg-base-200 rounded-lg p-8">
    <img
      v-if="imageUrl"
      :src="imageUrl"
      :alt="alt"
      class="max-w-full max-h-96 object-contain rounded-lg shadow-lg"
      @error="handleImageError"
    />
    <!-- 이미지 없을 때 기본 아이콘 -->
    <div v-else class="flex flex-col items-center justify-center text-base-content/30 py-20">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-32 w-32 mb-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
        />
      </svg>
      <span class="text-lg">이미지가 없습니다</span>
    </div>
  </figure>
</template>

<script setup>
import { ref, computed } from 'vue'

// ==================== Props ====================
const props = defineProps({
  image: {
    type: String,
    default: '',
  },
  alt: {
    type: String,
    default: '중고거래 이미지',
  },
})

// ==================== State ====================
const imageError = ref(false)

// ==================== Computed ====================
const imageUrl = computed(() => {
  if (!props.image || imageError.value) return ''
  if (props.image.startsWith('http')) return props.image
  return `http://localhost:8000${props.image}`
})

// ==================== Methods ====================
const handleImageError = () => {
  imageError.value = true
}
</script>
