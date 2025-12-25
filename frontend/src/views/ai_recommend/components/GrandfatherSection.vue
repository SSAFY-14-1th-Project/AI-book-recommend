<template>
  <!-- ==================== 할아버지 캐릭터 섹션 ==================== -->
  <div class="flex flex-col items-center justify-center">
    <!-- 할아버지 이미지 영역 -->
    <div class="relative w-full max-w-md">
      <!-- 할아버지 이미지 플레이스홀더 -->
      <!-- 실제 이미지로 교체하세요: <img src="/grandfather.png" alt="할아버지" /> -->
      <div class="aspect-square rounded-full bg-gradient-to-br from-amber-100 to-orange-200 flex items-center justify-center shadow-2xl border-8 border-base-100">
        <div class="text-center">
          <!-- 여기에 할아버지 이미지 에셋을 넣으세요 -->
          <div class="text-8xl mb-4">👴</div>
          <p class="text-2xl font-bold text-amber-900">동네책방</p>
          <p class="text-xl text-amber-800">할아버지</p>
        </div>
      </div>

      <!-- 로딩 중 애니메이션 -->
      <div v-if="isLoading" class="absolute -bottom-4 -right-4">
        <div class="bg-base-100 rounded-full p-3 shadow-lg border-2 border-primary">
          <span class="loading loading-dots loading-lg text-primary"></span>
        </div>
      </div>
    </div>

    <!-- 말풍선 -->
    <div class="w-full max-w-md mt-8">
      <div class="chat chat-start">
        <div class="chat-bubble chat-bubble-primary text-base-100 min-h-24 flex items-center">
          <p class="text-base leading-relaxed">
            <template v-if="isLoading">
              <span class="loading loading-dots loading-md"></span>
              할아버지가 책을 고르고 계십니다...
            </template>
            <template v-else-if="showFoundMessage">
              좋은 책들을 찾았네! 이 책들이 자네에게 딱 맞을 것 같아서 골라봤지. 아래로 내려가서 한번 읽어보게나!
            </template>
            <template v-else-if="hasRecommendations">
              이 책들이 자네에게 딱 맞을 것 같네. 오랜 경험으로 골라본 책들이니, 한번 읽어보게나!
            </template>
            <template v-else>
              어서 오게! 어떤 책을 찾고 있나? 60년 동안 쌓은 경험으로 자네에게 딱 맞는 책을 골라드리지!
            </template>
          </p>
        </div>
      </div>
    </div>

    <!-- 안내 메시지 -->
    <div class="alert alert-info shadow-sm max-w-md mt-6">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5 shrink-0"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <div class="text-sm">
        <p class="font-semibold">할아버지의 추천 비법</p>
        <p class="text-xs mt-1">
          오랜 경험과 당신의 독서 취향(MBTI)을 바탕으로 AI가 최적의 책 3권을 골라드립니다
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props ====================
defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  hasRecommendations: {
    type: Boolean,
    default: false,
  },
  showFoundMessage: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
/* 말풍선 애니메이션 */
.chat-bubble {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
