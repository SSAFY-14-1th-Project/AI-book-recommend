<template>
  <div class="relative w-12 h-16 drop-shadow-lg">
    <!-- 메달 배경 -->
    <svg class="w-full h-full" viewBox="0 0 80 100" xmlns="http://www.w3.org/2000/svg">
      <!-- 리본 -->
      <path d="M20 0 L30 0 L40 40 L30 35 L20 40 Z" fill="#ef4444" />
      <path d="M50 0 L60 0 L60 40 L50 35 L40 40 Z" fill="#dc2626" />
      <!-- 메달 원 -->
      <circle cx="40" cy="55" r="25" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5" />
      <circle cx="40" cy="55" r="22" fill="#fde68a" />
    </svg>
    <!-- 순위 텍스트 -->
    <div
      class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center justify-center mt-1"
    >
      <span class="text-md font-black leading-none text-amber-800 drop-shadow-sm">{{
        rankNumber
      }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  rankNumber: { type: Number, required: true },
})
</script>
