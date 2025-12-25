<template>
  <!-- ==================== 중고거래 검색 필터 영역 ==================== -->
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
        <option value="book">도서명</option>
        <option value="content">내용</option>
      </select>

      <!-- 검색어 입력 -->
      <div class="flex-1 relative">
        <input
          v-model="localFilters.search"
          type="text"
          placeholder="중고거래를 검색해보세요..."
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
    <div class="flex flex-col gap-4">
      <!-- 지역 필터 -->
      <div class="flex flex-wrap gap-2 items-start">
        <span class="text-sm font-semibold text-base-content/70 self-center mr-2"> 지역: </span>
        <button
          @click="toggleRegion(null)"
          :class="[
            'btn btn-sm',
            localFilters.regions.length === 0 ? 'btn-primary' : 'btn-outline btn-ghost',
          ]"
        >
          전체
        </button>
        <button
          v-for="region in regions"
          :key="region.value"
          @click="toggleRegion(region.value)"
          :class="[
            'btn btn-sm',
            localFilters.regions.includes(region.value) ? 'btn-primary' : 'btn-outline btn-ghost',
          ]"
        >
          {{ region.name }}
        </button>
      </div>

      <!-- 거래 타입 & 상태 & 가격 필터 -->
      <div class="flex flex-col lg:flex-row gap-4">
        <!-- 거래 타입 -->
        <div class="flex items-center gap-2">
          <label class="text-sm min-w-max font-semibold text-base-content/70">거래 타입:</label>
          <select
            v-model="localFilters.saleTypes"
            class="select select-bordered select-sm"
            @change="handleSaleTypeChange"
          >
            <option value="">전체</option>
            <option value="sell">판매</option>
            <option value="free">무료나눔</option>
          </select>
        </div>

        <!-- 거래 상태 -->
        <div class="flex items-center gap-2">
          <label class="text-sm min-w-max font-semibold text-base-content/70">상태:</label>
          <select
            v-model="localFilters.status"
            class="select select-bordered select-sm"
            @change="handleFilterChange"
          >
            <option value="">전체</option>
            <option value="available">판매중</option>
            <option value="reserved">예약중</option>
            <option value="sold">판매완료</option>
          </select>
        </div>

        <!-- 가격 범위 (무료나눔이 아닐 때만 표시) -->
        <div v-if="localFilters.saleTypes !== 'free'" class="flex items-center gap-2">
          <label class="min-w-max text-sm font-semibold text-base-content/70">가격:</label>
          <input
            v-model.number="localFilters.minPrice"
            type="number"
            placeholder="최소"
            class="input input-bordered input-sm w-24"
            min="0"
            @change="handleFilterChange"
          />
          <span class="text-base-content/70">~</span>
          <input
            v-model.number="localFilters.maxPrice"
            type="number"
            placeholder="최대"
            class="input input-bordered input-sm w-24"
            min="0"
            @change="handleFilterChange"
          />
        </div>
      </div>
    </div>

    <!-- 활성 필터 표시 -->
    <div
      v-if="hasActiveFilters"
      class="mt-4 pt-4 border-t border-base-300 flex items-center gap-2 flex-wrap"
    >
      <span class="text-sm text-base-content/70">활성 필터:</span>
      <div
        v-for="region in localFilters.regions"
        :key="region"
        class="badge badge-secondary badge-lg"
      >
        {{ getRegionName(region) }}
        <button @click="toggleRegion(region)" class="ml-2">✕</button>
      </div>
      <div v-if="localFilters.saleTypes" class="badge badge-accent badge-lg">
        {{ localFilters.saleTypes === 'sell' ? '판매' : '무료나눔' }}
      </div>
      <div v-if="localFilters.status" class="badge badge-info badge-lg">
        {{ getStatusText(localFilters.status) }}
      </div>
      <div
        v-if="localFilters.minPrice || localFilters.maxPrice"
        class="badge badge-warning badge-lg"
      >
        {{ formatPriceRange() }}
      </div>
      <button @click="clearAllFilters" class="btn btn-ghost btn-sm ml-auto">
        모든 필터 초기화
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ==================== Props & Emits ====================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'search'])

// ==================== 지역 데이터 ====================
const regions = [
  { value: 'seoul', name: '서울' },
  { value: 'busan', name: '부산' },
  { value: 'daegu', name: '대구' },
  { value: 'incheon', name: '인천' },
  { value: 'gwangju', name: '광주' },
  { value: 'daejeon', name: '대전' },
  { value: 'ulsan', name: '울산' },
  { value: 'sejong', name: '세종' },
  { value: 'gyeonggi', name: '경기' },
  { value: 'gangwon', name: '강원' },
  { value: 'chungbuk', name: '충북' },
  { value: 'chungnam', name: '충남' },
  { value: 'jeonbuk', name: '전북' },
  { value: 'jeonnam', name: '전남' },
  { value: 'gyeongbuk', name: '경북' },
  { value: 'gyeongnam', name: '경남' },
  { value: 'jeju', name: '제주' },
]

// ==================== 상태 관리 ====================
const localFilters = ref({
  search: props.modelValue.search || '',
  searchType: props.modelValue.searchType || 'title',
  regions: [...(props.modelValue.regions || [])],
  saleTypes: props.modelValue.saleTypes || '',
  status: props.modelValue.status || '',
  minPrice: props.modelValue.minPrice || null,
  maxPrice: props.modelValue.maxPrice || null,
})

// ==================== Computed ====================
// 활성 필터가 있는지 확인 (검색어 제외)
const hasActiveFilters = computed(() => {
  return (
    localFilters.value.regions.length > 0 ||
    localFilters.value.saleTypes ||
    localFilters.value.status ||
    localFilters.value.minPrice ||
    localFilters.value.maxPrice
  )
})

// ==================== Methods ====================
// 지역 토글
const toggleRegion = (regionValue) => {
  if (regionValue === null) {
    localFilters.value.regions = []
  } else {
    const index = localFilters.value.regions.indexOf(regionValue)
    if (index > -1) {
      localFilters.value.regions.splice(index, 1)
    } else {
      localFilters.value.regions.push(regionValue)
    }
  }
  handleFilterChange()
}

// 지역 이름 가져오기
const getRegionName = (regionValue) => {
  const region = regions.find((r) => r.value === regionValue)
  return region ? region.name : ''
}

// 상태 텍스트
const getStatusText = (status) => {
  const statusMap = {
    available: '판매중',
    reserved: '예약중',
    sold: '판매완료',
  }
  return statusMap[status] || status
}

// 가격 범위 포맷
const formatPriceRange = () => {
  const min = localFilters.value.minPrice
  const max = localFilters.value.maxPrice
  if (min && max) return `${min.toLocaleString()}원 ~ ${max.toLocaleString()}원`
  if (min) return `${min.toLocaleString()}원 이상`
  if (max) return `${max.toLocaleString()}원 이하`
  return ''
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
    regions: [],
    saleTypes: '',
    status: '',
    minPrice: null,
    maxPrice: null,
  }
  handleFilterChange()
}

// 필터 변경 시 부모 컴포넌트에 전달
const handleFilterChange = () => {
  emit('update:modelValue', {
    search: localFilters.value.search,
    searchType: localFilters.value.searchType,
    regions: [...localFilters.value.regions],
    saleTypes: localFilters.value.saleTypes,
    status: localFilters.value.status,
    minPrice: localFilters.value.minPrice,
    maxPrice: localFilters.value.maxPrice,
  })
}

// 거래 타입 변경 시 처리
const handleSaleTypeChange = () => {
  // 무료나눔 선택 시 가격 필터 초기화
  if (localFilters.value.saleTypes === 'free') {
    localFilters.value.minPrice = null
    localFilters.value.maxPrice = null
  }
  handleFilterChange()
}

// 가격 유효성 검사
const isPriceValid = () => {
  const { minPrice, maxPrice } = localFilters.value

  // 둘 다 없으면 유효
  if (!minPrice && !maxPrice) return true

  // 하나만 있으면 유효
  if (!minPrice || !maxPrice) return true

  // 둘 다 있으면 최소가 최대보다 작거나 같아야 함
  return minPrice <= maxPrice
}

// 검색 실행
const handleSearch = () => {
  // 가격 유효성 검사
  if (!isPriceValid()) {
    alert('최소 가격은 최대 가격보다 작거나 같아야 합니다.')
    return
  }

  handleFilterChange()
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
      regions: [...(newVal.regions || [])],
      saleTypes: newVal.saleTypes || '',
      status: newVal.status || '',
      minPrice: newVal.minPrice || null,
      maxPrice: newVal.maxPrice || null,
    }
  },
  { deep: true },
)
</script>
