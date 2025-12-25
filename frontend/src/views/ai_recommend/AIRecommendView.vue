<template>
  <main class="bg-base-100 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
      <!-- 헤더 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold mb-4">책방 할아버지께 물어봐!</h1>
        <p class="text-lg text-base-content/70">
          60년 경력의 동네책방 할아버지가 당신에게 딱 맞는 책을 추천해드립니다
        </p>
      </div>

      <!-- 할아버지 + 입력 폼 섹션 -->
      <div ref="grandfatherSection" class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <!-- 왼쪽: 할아버지 이미지 & 말풍선 -->
        <GrandfatherSection
          :is-loading="isLoading"
          :has-recommendations="recommendations.length > 0"
          :show-found-message="showFoundMessage"
        />

        <!-- 오른쪽: 입력 폼 -->
        <RecommendForm
          v-model:categories="selectedCategories"
          v-model:prompt="userPrompt"
          :is-loading="isLoading"
          @submit="handleSubmit"
        />
      </div>

      <!-- 추천 결과 -->
      <div v-if="recommendations.length > 0" ref="recommendationsSection" class="mt-12">
        <h2 class="text-2xl font-bold mb-6 text-center">
          할아버지가 추천하는 책들
        </h2>
        <RecommendationList
          :recommendations="recommendations"
          @book-click="handleBookClick"
        />
      </div>

      <!-- 에러 메시지 -->
      <div v-if="error" class="alert alert-error shadow-lg max-w-2xl mx-auto mt-8">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ error }}</span>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getAIRecommendation } from '@/api/book'
import GrandfatherSection from './components/GrandfatherSection.vue'
import RecommendForm from './components/RecommendForm.vue'
import RecommendationList from './components/RecommendationList.vue'

// ==================== 라우터 ====================
const router = useRouter()

// ==================== 상태 관리 ====================
const selectedCategories = ref([])
const userPrompt = ref('')
const isLoading = ref(false)
const recommendations = ref([])
const error = ref(null)
const showFoundMessage = ref(false)

// ==================== Refs ====================
const grandfatherSection = ref(null)
const recommendationsSection = ref(null)

// ==================== Scroll Helper ====================
const scrollToElement = (element, behavior = 'smooth') => {
  if (element) {
    element.scrollIntoView({ behavior, block: 'center' })
  }
}

// ==================== Methods ====================
const handleSubmit = async () => {
  if (!userPrompt.value.trim()) {
    error.value = '할아버지께 어떤 책을 찾으시는지 말씀해주세요'
    return
  }

  isLoading.value = true
  error.value = null
  showFoundMessage.value = false

  // 1️⃣ 할아버지 섹션으로 스크롤
  await nextTick()
  scrollToElement(grandfatherSection.value)

  try {
    const result = await getAIRecommendation({
      category_ids: selectedCategories.value,
      user_prompt: userPrompt.value,
    })

    // AI 응답 처리 (응답 형식에 따라 조정 필요)
    recommendations.value = result.recommendations || result

    if (recommendations.value.length === 0) {
      error.value = '할아버지가 추천할 책을 찾지 못했어요. 다른 조건으로 다시 물어봐주세요.'
    } else {
      // 2️⃣ 책을 찾았다는 말풍선 표시
      showFoundMessage.value = true

      // 3️⃣ 1초 후에 추천 도서 리스트로 스크롤
      setTimeout(async () => {
        await nextTick()
        scrollToElement(recommendationsSection.value)
      }, 1000)
    }
  } catch (err) {
    console.error('AI 추천 실패:', err)
    error.value = '할아버지께서 잠시 자리를 비우셨어요. 조금 후에 다시 물어봐주세요.'
  } finally {
    isLoading.value = false
  }
}

const handleBookClick = (bookId) => {
  router.push({ name: 'bookDetail', params: { id: bookId } })
}
</script>
