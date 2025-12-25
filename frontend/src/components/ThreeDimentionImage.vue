<template>
  <div class="hover-3d">
    <!-- 메인 이미지 (필수) -->
    <div v-for="image in images" :key="image.src">
      <img
        :src="image.src"
        :alt="image.alt || '이미지'"
        class="rounded-lg shadow-2xl w-full"
        loading="lazy"
        decoding="async"
      />
    </div>

    <!-- 추가 이미지들 (옵셔널) - 레이어 효과 -->
    <div v-for="_idx in blankLength" :key="_idx"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  images: {
    type: Array,
    required: true,
    validator: (value) => {
      // 최소 1개의 이미지 필요, 각 이미지는 src를 가져야 함
      return value.length >= 1 && value.every((img) => img.src && typeof img.src === 'string')
    },
  },
})

const blankLength = 8 - props.images.length
</script>

<style scoped></style>
