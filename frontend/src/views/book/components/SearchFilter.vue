<template>
  <!-- ==================== 검색 필터 영역 ==================== -->
  <div class="bg-base-100 shadow-lg rounded-lg p-6 mb-6">
    <!-- 검색바 섹션 -->
    <div class="flex flex-col lg:flex-row gap-4 mb-4">
      <!-- 검색 타입 선택 -->
      <select
        v-model="localFilters.searchType"
        class="select select-bordered w-full lg:w-40"
        @change="handleFilterChange"
      >
        <option value="title">제목</option>
        <option value="author">저자</option>
      </select>

      <!-- 검색어 입력 -->
      <div class="flex-1 relative">
        <input
          v-model="localFilters.search"
          type="text"
          placeholder="도서를 검색해보세요..."
          class="input input-bordered w-full pr-10"
          @keyup.enter="handleSearch"
        />
        <button
          v-if="localFilters.search"
          @click="clearSearch"
          class="btn btn-ghost btn-sm btn-circle absolute right-2 top-1/2 -translate-y-1/2"
        >
          ✕
        </button>
      </div>

      <!-- 검색 버튼 -->
      <button @click="handleSearch" class="btn btn-primary lg:w-32">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 mr-1"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        검색
      </button>
    </div>

    <!-- 필터 옵션 섹션 -->
    <div class="flex flex-col lg:flex-row gap-4 items-start lg:items-center">
      <!-- 카테고리 필터 -->
      <div class="flex flex-wrap gap-2 flex-1">
        <span class="text-sm font-semibold text-base-content/70 self-center mr-2">
          카테고리:
        </span>
        <button
          @click="toggleCategory(null)"
          :class="[
            'btn btn-sm',
            localFilters.categories.length === 0
              ? 'btn-primary'
              : 'btn-outline btn-ghost',
          ]"
        >
          전체
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          @click="toggleCategory(category.id)"
          :class="[
            'btn btn-sm',
            localFilters.categories.includes(category.id)
              ? 'btn-primary'
              : 'btn-outline btn-ghost',
          ]"
        >
          {{ category.name }}
        </button>
      </div>

      <!-- 성인 도서 필터 (조건부 표시) -->
      <div v-if="canViewAdultContent" class="flex items-center gap-2">
        <label class="label cursor-pointer gap-2">
          <span class="label-text">성인 도서 포함</span>
          <input
            v-model="localFilters.adult"
            type="checkbox"
            class="checkbox checkbox-primary"
            @change="handleFilterChange"
          />
        </label>
      </div>
    </div>

    <!-- 활성 필터 표시 -->
    <div
      v-if="hasActiveFilters"
      class="mt-4 pt-4 border-t border-base-300 flex items-center gap-2 flex-wrap"
    >
      <span class="text-sm text-base-content/70">활성 필터:</span>
      <div
        v-for="catId in localFilters.categories"
        :key="catId"
        class="badge badge-secondary badge-lg"
      >
        {{ getCategoryName(catId) }}
        <button @click="toggleCategory(catId)" class="ml-2">✕</button>
      </div>
      <div v-if="localFilters.adult" class="badge badge-accent badge-lg">
        성인 도서 포함
      </div>
      <button @click="clearAllFilters" class="btn btn-ghost btn-sm ml-auto">
        모든 필터 초기화
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useLoginStore } from '@/stores/loginStore'

// ==================== Props & Emits ====================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'search'])

// ==================== 카테고리 데이터 (하드코딩) ====================
const categories = [
  { id: 1, name: '소설/시/희곡' },
  { id: 2, name: '경제경영' },
  { id: 3, name: '자기계발' },
  { id: 4, name: '인문/교양' },
  { id: 5, name: '취미/실용' },
  { id: 6, name: '어린이/청소년' },
  { id: 7, name: '학습지' },
  { id: 8, name: '과학' },
]

// ==================== 상태 관리 ====================
const loginStore = useLoginStore()
const localFilters = ref({
  search: props.modelValue.search || '',
  searchType: props.modelValue.searchType || 'title',
  categories: [...(props.modelValue.categories || [])],
  adult: props.modelValue.adult || false,
})

// ==================== Computed ====================
// 성인 컨텐츠 열람 가능 여부 (로그인 + 나이 20세 이상)
const canViewAdultContent = computed(() => {
  if (!loginStore.user) return false
  const age = loginStore.user.age
  return age !== null && age >= 20
})

// 활성 필터가 있는지 확인 (검색어 제외)
const hasActiveFilters = computed(() => {
  return (
    localFilters.value.categories.length > 0 ||
    localFilters.value.adult
  )
})

// ==================== Methods ====================
// 카테고리 토글
const toggleCategory = (categoryId) => {
  if (categoryId === null) {
    localFilters.value.categories = []
  } else {
    const index = localFilters.value.categories.indexOf(categoryId)
    if (index > -1) {
      localFilters.value.categories.splice(index, 1)
    } else {
      localFilters.value.categories.push(categoryId)
    }
  }
  handleFilterChange()
}

// 카테고리 이름 가져오기
const getCategoryName = (categoryId) => {
  const category = categories.find((cat) => cat.id === categoryId)
  return category ? category.name : ''
}

// 검색어 초기화
const clearSearch = () => {
  localFilters.value.search = ''
  handleFilterChange()
}

// 모든 필터 초기화
const clearAllFilters = () => {
  localFilters.value = {
    search: '',
    searchType: 'title',
    categories: [],
    adult: false,
  }
  handleFilterChange()
}

// 필터 변경 시 부모 컴포넌트에 전달
const handleFilterChange = () => {
  emit('update:modelValue', {
    search: localFilters.value.search,
    searchType: localFilters.value.searchType,
    categories: [...localFilters.value.categories], // 배열 깊은 복사
    adult: localFilters.value.adult,
  })
}

// 검색 실행
const handleSearch = () => {
  // 검색 전에 필터 업데이트
  handleFilterChange()
  // 검색 이벤트 발생
  emit('search')
}

// ==================== Watch ====================
// 부모에서 필터가 변경되면 로컬 상태 업데이트
watch(
  () => props.modelValue,
  (newVal) => {
    localFilters.value = {
      search: newVal.search || '',
      searchType: newVal.searchType || 'title',
      categories: [...(newVal.categories || [])], // 배열 깊은 복사
      adult: newVal.adult || false,
    }
  },
  { deep: true }
)
</script>
