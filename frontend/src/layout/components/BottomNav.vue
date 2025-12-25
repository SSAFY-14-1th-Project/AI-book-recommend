<template>
  <!-- 모바일 하단 네비게이션 (832px 미만에서만 표시) -->
  <div
    class="min-[832px]:hidden fixed bottom-0 left-0 right-0 z-50 bg-base-100 border-t border-base-content/10 dock dock-lg"
  >
    <!-- 홈 -->
    <RouterLink
      :to="{ name: 'home' }"
      class="flex flex-col items-center justify-center"
      :class="{ 'dock-active text-primary': $route.name === 'home' }"
    >
      <HomeIcon class="w-6 h-6" />
      <span class="btm-nav-label text-xs">홈</span>
    </RouterLink>

    <!-- 도서 검색 -->
    <RouterLink
      :to="{ name: 'bookSearch' }"
      class="flex flex-col items-center justify-center"
      :class="{
        'dock-active text-primary': $route.name === 'bookSearch' || $route.name === 'bookDetail',
      }"
    >
      <MagnifyingGlassIcon class="w-6 h-6" />
      <span class="btm-nav-label text-xs">도서검색</span>
    </RouterLink>

    <!-- AI 추천 -->
    <RouterLink
      :to="{ name: 'aiRecommend' }"
      class="flex flex-col items-center justify-center"
      :class="{ 'dock-active text-primary': $route.name === 'aiRecommend' }"
    >
      <BookOpenIcon class="w-6 h-6" />
      <span class="btm-nav-label text-xs">AI추천</span>
    </RouterLink>

    <!-- 중고책 거래 -->
    <RouterLink
      :to="{ name: 'trade' }"
      class="flex flex-col items-center justify-center"
      :class="{ 'dock-active text-primary': $route.name?.startsWith('trade') }"
    >
      <BuildingStorefrontIcon class="w-6 h-6" />
      <span class="btm-nav-label text-xs">중고거래</span>
    </RouterLink>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import {
  HomeIcon,
  BookOpenIcon,
  BuildingStorefrontIcon,
  MagnifyingGlassIcon,
} from '@heroicons/vue/24/outline'

const $route = useRoute()
</script>

<style scoped>
/* iOS safe area 대응 */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}

/* active 상태 스타일 */
.btm-nav > .active {
  border-top: 2px solid currentColor;
}
</style>
