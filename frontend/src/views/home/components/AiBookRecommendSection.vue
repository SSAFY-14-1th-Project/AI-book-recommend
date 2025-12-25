<template>
  <!-- ==================== 할아버지 AI 추천 홍보 섹션 ==================== -->
  <section class="py-16 dark:from-amber-950/20 dark:to-orange-950/20">
    <div class="flex flex-col items-center gap-3 mb-10">
      <h2 class="text-3xl font-bold">책방 할아버지께 물어봐!</h2>
    </div>
    <div class="container mx-auto px-4">
      <div class="card bg-base-100 shadow-2xl overflow-hidden max-w-5xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-0">
          <!-- 왼쪽: 할아버지 이미지 영역 -->
          <div
            class="bg-linear-to-br from-amber-100 to-orange-200 dark:from-amber-900/50 dark:to-orange-900/50 flex items-center justify-center p-12 relative overflow-hidden"
          >
            <!-- 배경 장식 -->
            <div class="absolute inset-0 opacity-10">
              <div class="absolute top-10 left-10 text-6xl">📚</div>
              <div class="absolute bottom-10 right-10 text-6xl">📖</div>
              <div class="absolute top-1/2 left-1/4 text-4xl">✨</div>
            </div>

            <!-- 할아버지 캐릭터 -->
            <div class="relative z-10 text-center">
              <div
                class="w-48 h-48 mx-auto mb-6 rounded-full bg-linear-to-br from-amber-200 to-orange-300 flex items-center justify-center shadow-xl border-8 border-white/50 animate-float"
              >
                <div class="text-8xl">👴</div>
              </div>
              <div class="space-y-2">
                <p class="text-2xl font-bold text-amber-900 dark:text-amber-100">동네책방</p>
                <p class="text-xl text-amber-800 dark:text-amber-200">할아버지</p>
                <div class="badge badge-warning gap-2 text-sm px-4 py-3">
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
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                  60년 경력
                </div>
              </div>
            </div>
          </div>

          <!-- 오른쪽: 설명 및 버튼 영역 -->
          <div class="card-body p-12 flex flex-col justify-center">
            <p class="text-lg text-base-content/80 mb-6 leading-relaxed">
              60년 동안 책과 함께한 동네책방 할아버지가<br />
              당신에게 딱 맞는 책을 골라드립니다
            </p>

            <!-- 특징 리스트 -->
            <div class="space-y-3 mb-8">
              <div class="flex items-start gap-3">
                <div class="badge badge-primary badge-lg shrink-0 mt-1">✓</div>
                <p class="text-base">
                  <span class="font-semibold">AI 기반 맞춤 추천</span><br />
                  <span class="text-sm text-base-content/70"
                    >당신의 독서 취향을 분석해 최적의 책 3권 추천</span
                  >
                </p>
              </div>
              <div class="flex items-start gap-3">
                <div class="badge badge-primary badge-lg shrink-0 mt-1">✓</div>
                <p class="text-base">
                  <span class="font-semibold">따뜻한 할아버지의 조언</span><br />
                  <span class="text-sm text-base-content/70"
                    >오랜 경험으로 책을 고르는 이유를 친절히 설명</span
                  >
                </p>
              </div>
              <div class="flex items-start gap-3">
                <div class="badge badge-primary badge-lg shrink-0 mt-1">✓</div>
                <p class="text-base">
                  <span class="font-semibold">무료 서비스</span><br />
                  <span class="text-sm text-base-content/70">언제든지 할아버지께 물어보세요!</span>
                </p>
              </div>
            </div>

            <!-- CTA 버튼 -->
            <div class="card-actions">
              <button @click="goToAIRecommend" class="btn btn-primary btn-lg w-full group">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 group-hover:animate-bounce"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
                할아버지께 물어보러 가기
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 group-hover:translate-x-1 transition-transform"
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
              </button>
            </div>

            <!-- 안내 문구 -->
            <p class="text-xs text-center text-base-content/50 mt-4">
              💡 로그인하면 Book MBTI 기반 추천을 받을 수 있어요
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToAIRecommend = () => {
  router.push({ name: 'aiRecommend' })
}
</script>

<style scoped>
/* 할아버지 이미지 떠다니는 애니메이션 */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>
