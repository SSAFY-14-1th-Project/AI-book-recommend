<template>
  <!-- ==================== 도서 검색 페이지 ==================== -->
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- 페이지 헤더 -->
    <div class="mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-base-content mb-2">도서 검색</h1>
      <p class="text-base-content/70">원하는 도서를 검색하고 탐색해보세요</p>
    </div>

    <!-- 검색 필터 -->
    <SearchFilter v-model="filters" @search="handleSearch" />

    <!-- 검색 결과 헤더 -->
    <div v-if="!loading && searchPerformed" class="flex items-center justify-between mb-6">
      <div class="text-lg font-semibold">
        <span v-if="books.length > 0">
          검색 결과: <span class="text-primary">{{ totalCount }}</span
          >권
        </span>
        <span v-else class="text-base-content/50"> 검색 결과가 없습니다 </span>
      </div>
    </div>

    <!-- 도서 그리드 -->
    <BookGrid v-if="searchPerformed" :books="books" :loading="loading" :skeleton-count="pageSize" />

    <!-- 페이지네이션 -->
    <BookPagination
      v-if="!loading && books.length > 0"
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
      <h2 class="text-2xl font-bold text-base-content/60 mb-3">도서를 검색해보세요</h2>
      <p class="text-base-content/40 max-w-md">
        검색어를 입력하거나 카테고리를 선택하여 원하는 도서를 찾아보세요.
        <br />
        검색 버튼을 눌러 모든 도서를 조회할 수도 있습니다.
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
import { ref, onMounted, onUnmounted, onActivated, onDeactivated, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { searchBooks } from '@/api/book'
import SearchFilter from './components/SearchFilter.vue'
import BookGrid from './components/BookGrid.vue'
import BookPagination from './components/BookPagination.vue'

// keep-alive 캐싱을 위한 컴포넌트 이름 설정
defineOptions({
  name: 'BookView',
})

// ==================== 라우터 ====================
const router = useRouter()
const route = useRoute()

// ==================== 상태 관리 ====================
const loading = ref(false)
const searchPerformed = ref(false)
const books = ref([])
const currentPage = ref(1)
const totalPages = ref(0)
const totalCount = ref(0)
const pageSize = ref(20)
const showScrollTop = ref(false)

// 검색 필터 상태
const filters = ref({
  search: '',
  searchType: 'title',
  categories: [],
  adult: false,
})

// ==================== URL 쿼리 파라미터 관리 ====================
// URL에서 상태 읽기
const loadStateFromQuery = () => {
  const query = route.query

  // 검색어 (없으면 기본값으로 초기화)
  filters.value.search = query.search || ''

  // 검색 타입 (없으면 기본값)
  filters.value.searchType = query.searchType || 'title'

  // 카테고리 (쉼표로 구분된 문자열 -> 숫자 배열)
  if (query.categories) {
    const categoriesStr = query.categories
    filters.value.categories = categoriesStr
      .split(',')
      .map(Number)
      .filter((n) => !isNaN(n))
  } else {
    filters.value.categories = []
  }

  // 성인 도서 (없으면 기본값)
  filters.value.adult = query.adult === 'true'

  // 페이지 번호 (없으면 1)
  currentPage.value = query.page ? Number(query.page) : 1

  // 페이지당 개수 (없으면 20)
  pageSize.value = query.size ? Number(query.size) : 20

  // 검색 수행 여부
  searchPerformed.value = query.searched === 'true'
}

// 상태를 URL에 저장
const saveStateToQuery = () => {
  const query = {}

  // 검색어가 있을 때만 저장
  if (filters.value.search) {
    query.search = filters.value.search
    query.searchType = filters.value.searchType
  }

  // 카테고리가 있을 때만 저장 (배열 -> 쉼표로 구분된 문자열)
  if (filters.value.categories.length > 0) {
    query.categories = filters.value.categories.join(',')
  }

  // 성인 도서 필터가 true일 때만 저장
  if (filters.value.adult) {
    query.adult = 'true'
  }

  // 페이지 번호 (1이 아닐 때만)
  if (currentPage.value !== 1) {
    query.page = currentPage.value
  }

  // 페이지당 개수 (20이 아닐 때만)
  if (pageSize.value !== 20) {
    query.size = pageSize.value
  }

  // 검색을 수행했다는 플래그
  if (searchPerformed.value) {
    query.searched = 'true'
  }

  // URL 업데이트 (페이지 리로드 없이)
  router.replace({ query })
}

// ==================== Methods ====================
// 도서 검색 API 호출
const fetchBooks = async () => {
  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
    }

    // 검색어가 있을 때만 추가
    if (filters.value.search) {
      params.search = filters.value.search
      params.searchType = filters.value.searchType
    }

    // 카테고리 필터가 있을 때만 추가 (Proxy 객체를 일반 배열로 변환)
    if (filters.value.categories.length > 0) {
      params.categories = [...filters.value.categories]
    }

    // 성인 도서 필터
    params.adult = filters.value.adult

    const response = await searchBooks(params)

    books.value = response.results || []
    totalPages.value = response.totalPages || 0
    totalCount.value = response.count || 0
    searchPerformed.value = true

    // 검색 후 URL에 상태 저장
    saveStateToQuery()
  } catch (error) {
    console.error('도서 검색 실패:', error)
    books.value = []
    totalPages.value = 0
    totalCount.value = 0

    // 에러 알림
    alert('도서 검색에 실패했습니다. 다시 시도해주세요.')
  } finally {
    loading.value = false
  }
}

// 검색 실행
const handleSearch = () => {
  currentPage.value = 1
  fetchBooks()
  scrollToTop()
}

// 페이지 변경
const handlePageChange = (page) => {
  currentPage.value = page
  fetchBooks()
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
  // URL에서 상태 복원
  loadStateFromQuery()

  // URL에 검색 파라미터가 있으면 자동으로 검색 실행
  if (route.query.searched === 'true') {
    fetchBooks()
  }

  // 스크롤 이벤트 리스너 등록
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  // 스크롤 이벤트 리스너 제거
  window.removeEventListener('scroll', handleScroll)
})

// keep-alive 전용 훅
onActivated(() => {
  // 활성화될 때 URL에서 상태 복원
  loadStateFromQuery()
})

onDeactivated(() => {
  // 다음 라우트 확인
  // BookDetail(/books/:id)로 이동하는 게 아니면 상태 초기화
  setTimeout(() => {
    const currentPath = router.currentRoute.value.path

    // /books/:id 형식이 아니면 상태 초기화
    if (!currentPath.match(/^\/books\/\d+$/)) {
      // 검색 상태 초기화
      searchPerformed.value = false
      books.value = []
      currentPage.value = 1
      totalPages.value = 0
      totalCount.value = 0
      filters.value = {
        search: '',
        searchType: 'title',
        categories: [],
        adult: false,
      }
    } else {
      console.log('[BookView] 상태 유지 (BookDetail로 이동)')
    }
  }, 0)
})

// ==================== Watch ====================
// 브라우저 뒤로가기/앞으로가기 감지
// deep: false로 설정하여 무한 루프 방지
watch(
  () => route.query,
  (newQuery, oldQuery) => {
    // 같은 쿼리면 무시 (무한 루프 방지)
    if (JSON.stringify(newQuery) === JSON.stringify(oldQuery)) {
      return
    }

    // URL에서 상태 복원
    loadStateFromQuery()

    // 검색이 수행된 상태이면 데이터 가져오기
    if (newQuery.searched === 'true') {
      // fetchBooks는 내부에서 saveStateToQuery를 호출하므로
      // 무한 루프를 막기 위해 조건 확인
      const needsFetch =
        newQuery.page !== oldQuery?.page ||
        newQuery.size !== oldQuery?.size ||
        newQuery.search !== oldQuery?.search ||
        newQuery.searchType !== oldQuery?.searchType ||
        newQuery.categories !== oldQuery?.categories ||
        newQuery.adult !== oldQuery?.adult

      if (needsFetch) {
        fetchBooks()
      }
    }
  },
)
</script>
