<template>
  <section class="py-16 space-y-16">
    <!-- 섹션 헤더 -->
    <div class="flex flex-col items-center gap-3 mb-10">
      <h2 class="text-3xl font-bold">추천 도서</h2>
      <p class="text-md text-base-content/70">알라딘 인기 도서와 동네책방 사용자들이 선택한 베스트 도서를 만나보세요!</p>
    </div>

    <!-- 알라딘 베스트셀러 -->
    <BookCaracel
      title="📚 알라딘 베스트셀러"
      description="알라딘 사이트 선정 최고의 도서!"
      :books="bestSellers"
      :loading="bestSellersDataLoading"
    />

    <!-- 높은 평점 도서 -->
    <!-- <BookCaracel
      title="⭐ 높은 평점 도서"
      description="독자들이 가장 높게 평가한 책들"
      :books="highRatedBooks"
      :loading="highRatedBooksLoading"
    /> -->

    <!-- 최신 출간 도서 -->
    <BookCaracel
      title="🆕 최신 출간 도서"
      description="갓 출간된 신간 도서를 만나보세요"
      :books="newReleaseBooks"
      :loading="newReleaseBooksLoading"
    />
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import BookCaracel from '@/components/BookCaracel.vue'
import { getBestSellerList, searchBooks } from '@/api/book'

// 베스트셀러
const bestSellers = ref([])
const bestSellersDataLoading = ref(true)

// 높은 평점 도서
const highRatedBooks = ref([])
const highRatedBooksLoading = ref(true)

// 최신 출간 도서
const newReleaseBooks = ref([])
const newReleaseBooksLoading = ref(true)

onMounted(async () => {
  // 베스트셀러 가져오기
  try {
    const bestSellersData = await getBestSellerList()
    bestSellers.value = bestSellersData
  } catch (error) {
    console.error('베스트셀러 로드 실패:', error)
  } finally {
    bestSellersDataLoading.value = false
  }

  // 높은 평점 도서 가져오기 (검색 API 활용)
  try {
    const highRatedData = await searchBooks({
      page: 1,
      size: 10,
    })
    // 평점순으로 정렬 (클라이언트 사이드)
    highRatedBooks.value = highRatedData.results
      .filter(book => book.customerReviewRank >= 9)
      .slice(0, 10)
  } catch (error) {
    console.error('높은 평점 도서 로드 실패:', error)
  } finally {
    highRatedBooksLoading.value = false
  }

  // 최신 출간 도서 가져오기
  try {
    const newReleaseData = await searchBooks({
      page: 1,
      size: 20,
    })
    // 출판일 기준 정렬 (클라이언트 사이드)
    newReleaseBooks.value = newReleaseData.results
      .filter(book => book.pubDate)
      .sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate))
      .slice(0, 10)
  } catch (error) {
    console.error('최신 도서 로드 실패:', error)
  } finally {
    newReleaseBooksLoading.value = false
  }
})
</script>
