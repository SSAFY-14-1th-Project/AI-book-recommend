<template>
  <!-- ==================== 추천 요청 폼 ==================== -->
  <div class="card bg-base-100 shadow-xl border border-base-content/10">
    <div class="card-body p-8">
      <h3 class="text-2xl font-bold mb-6">어떤 책을 찾으시나요?</h3>

      <form @submit.prevent="$emit('submit')" class="space-y-6">
        <!-- 카테고리 선택 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium text-base"> 관심 분야 (선택사항) </span>
            <span class="label-text-alt text-base-content/50">
              {{ selectedCategories.length }}개 선택됨
            </span>
          </label>
          <div class="grid grid-cols-2 gap-2">
            <label
              v-for="category in categories"
              :key="category.id"
              class="label cursor-pointer justify-start gap-3 bg-base-200/50 rounded-lg px-4 py-3 hover:bg-base-300 transition-colors"
            >
              <input
                type="checkbox"
                :value="category.id"
                v-model="selectedCategories"
                class="checkbox checkbox-primary checkbox-sm"
              />
              <span class="label-text">{{ category.name }}</span>
            </label>
          </div>
          <label class="label">
            <span class="label-text-alt text-base-content/60">
              선택하지 않으면 전체 분야에서 추천합니다
            </span>
          </label>
        </div>

        <!-- 사용자 요청 -->
        <div class="form-control flex flex-col">
          <label class="label">
            <span class="label-text font-medium text-base">
              할아버지께 하고 싶은 말
              <span class="text-error ml-1">*</span>
            </span>
            <span class="label-text-alt text-base-content/50"> {{ userPrompt.length }}/500 </span>
          </label>
          <textarea
            :value="prompt"
            @input="$emit('update:prompt', $event.target.value)"
            placeholder="예: 요즘 마음이 힘들어요. 위로가 되는 따뜻한 책을 추천해주세요.&#10;예: 새로운 취미를 시작하고 싶어요. 쉽게 읽히는 실용서를 추천해주세요."
            class="textarea textarea-bordered h-32 resize-none focus:textarea-primary w-full"
            required
          ></textarea>
          <label class="label">
            <span class="label-text-alt text-base-content/60 text-wrap">
              구체적으로 말씀해주실수록 더 좋은 추천을 받을 수 있습니다
            </span>
          </label>
        </div>

        <!-- 제출 버튼 -->
        <button
          type="submit"
          class="btn btn-primary w-full btn-lg"
          :disabled="isLoading || !prompt.trim()"
        >
          <svg
            v-if="!isLoading"
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
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
          <span v-if="isLoading" class="loading loading-spinner"></span>
          {{ isLoading ? '할아버지께서 고민 중...' : '할아버지께 물어보기' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// ==================== Props & Emits ====================
const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  prompt: {
    type: String,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:categories', 'update:prompt', 'submit'])

// ==================== 로컬 상태 ====================
const selectedCategories = computed({
  get: () => props.categories,
  set: (value) => emit('update:categories', value),
})

const userPrompt = computed(() => props.prompt)

// ==================== 카테고리 목록 (하드코딩 - 실제로는 API에서 가져와야 함) ====================
const categories = [
  { id: 1, name: '소설' },
  { id: 2, name: '시/에세이' },
  { id: 3, name: '인문' },
  { id: 4, name: '가정/육아' },
  { id: 5, name: '요리' },
  { id: 6, name: '건강' },
  { id: 7, name: '취미/실용/스포츠' },
  { id: 8, name: '경제/경영' },
  { id: 9, name: '자기계발' },
  { id: 10, name: '정치/사회' },
  { id: 11, name: '역사/문화' },
  { id: 12, name: '종교' },
  { id: 13, name: '예술/대중문화' },
  { id: 14, name: '중/고등참고서' },
  { id: 15, name: '기술/공학' },
  { id: 16, name: '외국어' },
  { id: 17, name: '과학' },
  { id: 18, name: '취업/수험서' },
  { id: 19, name: '여행' },
  { id: 20, name: '컴퓨터/IT' },
]
</script>
