<template>
  <main class="bg-base-100 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
      <!-- 헤더 -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold">마이페이지</h1>
        <p class="text-base-content/60 mt-2">내 정보와 북마크한 도서를 확인하세요</p>
      </div>

      <!-- 로딩 중 -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <!-- 컨텐츠 -->
      <div v-else class="grid grid-cols-1 gap-8">
        <!-- 사용자 정보 -->
        <div>
          <UserInfoCard :user="user" @edit="handleEditProfile" />
        </div>

        <!-- 북마크 목록 -->
        <div>
          <BookmarkList
            :bookmarks="bookmarks"
            :loading="bookmarksLoading"
            @book-click="handleBookClick"
          />
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/loginStore'
import { getBookmarkedBooks } from '@/api/book'
import UserInfoCard from './components/UserInfoCard.vue'
import BookmarkList from './components/BookmarkList.vue'

// ==================== 라우터 & 스토어 ====================
const router = useRouter()
const loginStore = useLoginStore()

// ==================== 상태 관리 ====================
const loading = ref(false)
const bookmarksLoading = ref(false)
const user = ref(null)
const bookmarks = ref([])

// ==================== Methods ====================
// 프로필 수정 페이지로 이동
const handleEditProfile = () => {
  router.push({ name: 'onboard', query: { edit: 'true' } })
}

// 도서 상세 페이지로 이동
const handleBookClick = (bookId) => {
  router.push({ name: 'bookDetail', params: { id: bookId } })
}

// 북마크 목록 조회
const fetchBookmarks = async () => {
  bookmarksLoading.value = true
  try {
    const data = await getBookmarkedBooks()
    bookmarks.value = data
  } catch (error) {
    console.error('북마크 조회 실패:', error)
    bookmarks.value = []
  } finally {
    bookmarksLoading.value = false
  }
}

// ==================== Lifecycle ====================
onMounted(async () => {
  loading.value = true

  // 사용자 정보 로드 (loginStore에서)
  user.value = loginStore.user

  // 북마크 목록 로드
  await fetchBookmarks()

  loading.value = false
})
</script>
