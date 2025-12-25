<template>
  <!-- ==================== 중고거래 검색 페이지 ==================== -->
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- 페이지 헤더 -->
    <div class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-3xl md:text-4xl font-bold text-base-content mb-2">중고거래</h1>
        <p class="text-base-content/70">원하는 중고 도서를 검색하고 거래해보세요</p>
      </div>
      <RouterLink :to="{ name: 'tradeCreate' }" class="btn btn-primary">
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
            d="M12 4v16m8-8H4"
          />
        </svg>
        거래 등록
      </RouterLink>
    </div>

    <!-- 검색 필터 -->
    <TradeSearchFilter v-model="filters" @search="handleSearch" />

    <!-- 검색 결과 헤더 -->
    <div v-if="!loading && searchPerformed" class="flex items-center justify-between mb-6">
      <div class="text-lg font-semibold">
        <span v-if="trades.length > 0">
          검색 결과: <span class="text-primary">{{ totalCount }}</span
          >개
        </span>
        <span v-else class="text-base-content/50"> 검색 결과가 없습니다 </span>
      </div>
    </div>

    <!-- 거래 그리드 -->
    <TradeGrid
      v-if="searchPerformed"
      :trades="trades"
      :loading="loading"
      :skeleton-count="pageSize"
    />

    <!-- 페이지네이션 -->
    <TradePagination
      v-if="!loading && trades.length > 0"
      v-model:current-page="currentPage"
      v-model:totalPages="totalPages"
      :total-count="totalCount"
      @update:current-page="handlePageChange"
    />

    <!-- 초기 안내 메시지 (검색 전) -->
    <div
      v-if="!loading && !searchPerformed"
      class="flex flex-col items-center justify-center py-20 text-center"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-32 w-32 text-primary/30 mb-6"
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
      <h2 class="text-2xl font-bold text-base-content/60 mb-3">중고거래를 검색해보세요</h2>
      <p class="text-base-content/40 max-w-md">
        검색어를 입력하거나 필터를 선택하여 원하는 중고 도서를 찾아보세요.
        <br />
        검색 버튼을 눌러 모든 거래를 조회할 수도 있습니다.
      </p>
    </div>

    <!-- 맨 위로 버튼 -->
    <button
      v-if="showScrollTop"
      @click="scrollToTop"
      class="btn btn-circle btn-primary fixed bottom-8 right-8 shadow-lg z-50"
      aria-label="맨 위로"
    >
      <svg
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
          d="M5 10l7-7m0 0l7 7m-7-7v18"
        />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { searchTrades } from '@/api/trades'
import TradeSearchFilter from './components/TradeSearchFilter.vue'
import TradeGrid from './components/TradeGrid.vue'
import TradePagination from './components/TradePagination.vue'

// ==================== 라우터 ====================
const router = useRouter()
const route = useRoute()

// ==================== 상태 관리 ====================
const loading = ref(false)
const searchPerformed = ref(false)
const trades = ref([])
const currentPage = ref(1)
const totalPages = ref(0)
const totalCount = ref(0)
const pageSize = ref(20)
const showScrollTop = ref(false)

// 검색 필터 상태
const filters = ref({
  search: '',
  searchType: 'title',
  regions: [],
  saleTypes: '',
  status: '',
  minPrice: null,
  maxPrice: null,
})

// ==================== URL 쿼리 파라미터 관리 ====================
// URL에서 상태 읽기
const loadStateFromQuery = () => {
  const query = route.query

  filters.value.search = query.search || ''
  filters.value.searchType = query.searchType || 'title'

  // 지역 (쉼표로 구분된 문자열 -> 배열)
  if (query.regions) {
    filters.value.regions = query.regions.split(',')
  } else {
    filters.value.regions = []
  }

  filters.value.saleTypes = query.saleTypes || ''
  filters.value.status = query.status || ''
  filters.value.minPrice = query.minPrice ? Number(query.minPrice) : null
  filters.value.maxPrice = query.maxPrice ? Number(query.maxPrice) : null

  currentPage.value = query.page ? Number(query.page) : 1
  pageSize.value = query.size ? Number(query.size) : 20
  searchPerformed.value = query.searched === 'true'
}

// 상태를 URL에 저장
const saveStateToQuery = () => {
  const query = {}

  if (filters.value.search) {
    query.search = filters.value.search
    query.searchType = filters.value.searchType
  }

  if (filters.value.regions.length > 0) {
    query.regions = filters.value.regions.join(',')
  }

  if (filters.value.saleTypes) {
    query.saleTypes = filters.value.saleTypes
  }

  if (filters.value.status) {
    query.status = filters.value.status
  }

  if (filters.value.minPrice) {
    query.minPrice = filters.value.minPrice
  }

  if (filters.value.maxPrice) {
    query.maxPrice = filters.value.maxPrice
  }

  if (currentPage.value !== 1) {
    query.page = currentPage.value
  }

  if (pageSize.value !== 20) {
    query.size = pageSize.value
  }

  if (searchPerformed.value) {
    query.searched = 'true'
  }

  router.replace({ query })
}

// ==================== Methods ====================
// 거래 검색 API 호출
const fetchTrades = async () => {
  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
    }

    if (filters.value.search) {
      params.search = filters.value.search
      params.searchType = filters.value.searchType
    }

    // 지역 필터 (백엔드는 region 단수형 사용)
    if (filters.value.regions.length > 0) {
      params.region = [...filters.value.regions]
    }

    // 거래 타입 필터 (백엔드는 saleType 단수형 사용, 값은 sale/free)
    if (filters.value.saleTypes) {
      params.saleType = filters.value.saleTypes === 'sell' ? 'sale' : filters.value.saleTypes
    }

    if (filters.value.status) {
      params.status = filters.value.status
    }

    // 무료나눔이 아닐 때만 가격 파라미터 추가
    if (filters.value.saleTypes !== 'free') {
      if (filters.value.minPrice) {
        params.minPrice = filters.value.minPrice
      }

      if (filters.value.maxPrice) {
        params.maxPrice = filters.value.maxPrice
      }
    }

    console.log(params)

    const response = await searchTrades(params)

    trades.value = response.data.results || []
    totalPages.value = response.data.totalPages || 0
    totalCount.value = response.data.count || 0
    searchPerformed.value = true

    saveStateToQuery()
  } catch (error) {
    console.error('중고거래 검색 실패:', error)
    trades.value = []
    totalPages.value = 0
    totalCount.value = 0

    alert('중고거래 검색에 실패했습니다. 다시 시도해주세요.')
  } finally {
    loading.value = false
  }
}

// 검색 실행
const handleSearch = () => {
  currentPage.value = 1
  fetchTrades()
  scrollToTop()
}

// 페이지 변경
const handlePageChange = (page) => {
  currentPage.value = page
  fetchTrades()
  scrollToTop()
}

// 맨 위로 스크롤
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  showScrollTop.value = window.scrollY > 300
}

// ==================== Lifecycle ====================
onMounted(() => {
  loadStateFromQuery()

  if (route.query.searched === 'true') {
    fetchTrades()
  }

  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// ==================== Watch ====================
// 브라우저 뒤로가기/앞으로가기 감지
watch(
  () => route.query,
  (newQuery, oldQuery) => {
    if (JSON.stringify(newQuery) === JSON.stringify(oldQuery)) {
      return
    }

    loadStateFromQuery()

    if (newQuery.searched === 'true') {
      const needsFetch =
        newQuery.page !== oldQuery?.page ||
        newQuery.size !== oldQuery?.size ||
        newQuery.search !== oldQuery?.search ||
        newQuery.searchType !== oldQuery?.searchType ||
        newQuery.regions !== oldQuery?.regions ||
        newQuery.saleTypes !== oldQuery?.saleTypes ||
        newQuery.status !== oldQuery?.status ||
        newQuery.minPrice !== oldQuery?.minPrice ||
        newQuery.maxPrice !== oldQuery?.maxPrice

      if (needsFetch) {
        fetchTrades()
      }
    }
  },
)
</script>
