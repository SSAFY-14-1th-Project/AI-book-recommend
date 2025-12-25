<template>
  <main class="bg-base-100 min-h-screen">
    <div v-if="book.id" class="container mx-auto px-4 py-8 max-w-6xl">
      <!-- 상단: 제목, 저자, 출판사, 카테고리, 북마크 -->
      <div class="pb-6 mb-8 border-b border-base-content/10">
        <div class="flex justify-between items-start gap-4">
          <!-- 왼쪽: 도서 기본 정보 -->
          <div class="flex-1">
            <h1 class="text-3xl font-bold text-base-content mb-4">{{ book.title }}</h1>
            <div class="flex flex-wrap gap-2 text-base-content/70 text-lg">
              <span>{{ book.author }}</span>
              <span>·</span>
              <span>{{ book.publisher }}</span>
              <span>·</span>
              <span>{{ book.pubDate }}</span>
            </div>
            <div class="mt-4">
              <span class="badge badge-primary badge-md">{{ book.category?.name }}</span>
            </div>
          </div>

          <!-- 오른쪽: 북마크 버튼 -->
          <button
            @click="handleBookmark(book.id)"
            class="btn btn-circle btn-lg"
            :class="book.isBookmarked ? 'btn-error' : 'btn-ghost'"
          >
            <BookmarkIconSolid v-if="book.isBookmarked" class="w-8 h-8" />
            <BookmarkIcon v-else class="w-8 h-8" />
          </button>
        </div>
      </div>

      <!-- 중간: 도서 이미지 & 상세 정보 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 pb-8 mb-8 border-b border-base-content/10">
        <!-- 왼쪽: 도서 이미지 -->
        <figure class="flex justify-center items-start">
          <ThreeDimentionImage :images="[{ src: book.cover, alt: `${book.title} 커버 이미지` }]" />
        </figure>

        <!-- 오른쪽: 상세 정보 -->
        <div class="flex flex-col gap-8">
          <!-- 평점 & 순위 정보 -->
          <div class="space-y-4">
            <h3 class="text-xl font-bold border-b border-base-content/10 pb-2">평가 및 순위</h3>
            <div class="grid grid-cols-1 gap-4">
              <div class="flex justify-between items-center py-3 border-b border-base-content/5">
                <span class="text-base-content/70">알라딘 평점</span>
                <span class="text-2xl font-bold"
                  >{{ book.customerReviewRank
                  }}<span class="text-sm text-base-content/50">/10</span></span
                >
              </div>
              <div class="flex justify-between items-center py-3 border-b border-base-content/5">
                <span class="text-base-content/70">알라딘 베스트셀러 순위</span>
                <span class="text-2xl font-bold"
                  >{{ book.bestRank || '-'
                  }}<span class="text-sm text-base-content/50">위</span></span
                >
              </div>
              <div class="flex justify-between items-center py-3">
                <span class="text-base-content/70">동네책방 사용자 평가</span>
                <div class="text-right">
                  <div class="text-2xl font-bold">{{ book.averageRating }}</div>
                  <div class="text-sm text-base-content/50">{{ book.ratingCount }}개의 평가</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 가격 정보 -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 border-b border-base-content/10 pb-2">
              <h3 class="text-xl font-bold flex-1">알라딘 가격 정보</h3>
              <a
                :href="`https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=${book.itemId}`"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-ghost btn-sm btn-circle"
                title="알라딘 도서 페이지로 이동"
              >
                <ArrowTopRightOnSquareIcon class="w-5 h-5" />
              </a>
            </div>
            <div class="flex items-center justify-between py-3">
              <div class="flex flex-col gap-2">
                <span class="text-sm text-base-content/60 line-through">
                  정가: {{ book.priceStandard?.toLocaleString() }}원
                </span>
                <span class="text-3xl font-bold text-error">
                  {{ book.priceSales?.toLocaleString() }}원
                </span>
              </div>
              <div class="badge badge-error badge-lg h-12 text-lg">
                {{
                  Math.round(((book.priceStandard - book.priceSales) / book.priceStandard) * 100)
                }}% 할인
              </div>
            </div>
          </div>

          <!-- 도서 설명 -->
          <div class="space-y-3">
            <h3 class="text-xl font-bold border-b border-base-content/10 pb-2">도서 소개</h3>
            <p v-if="book.description" class="text-base-content/80 leading-relaxed">
              {{ book.description }}
            </p>
            <p v-else class="text-base-content/60 italic">도서 소개가 제공되지 않습니다.</p>
          </div>
        </div>
      </div>

      <!-- 하단 섹션: 중고 거래 정보 -->
      <div class="pt-4">
        <div class="flex items-center justify-between mb-6 border-b border-base-content/10 pb-3">
          <h2 class="text-2xl font-bold">동네책방 중고 거래</h2>
          <span v-if="book.trades && book.trades.length > 0" class="badge badge-primary badge-lg">
            {{ book.trades.length }}건
          </span>
        </div>

        <!-- 중고 거래 목록 그리드 -->
        <div v-if="book.trades && book.trades.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <TradeCard
            v-for="trade in book.trades"
            :key="trade.id"
            :trade="trade"
          />
        </div>

        <!-- 중고 거래 없을 때 -->
        <div v-else class="alert alert-info">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="stroke-current shrink-0 w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span>현재 등록된 중고 거래가 없습니다.</span>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="flex justify-center items-center min-h-screen">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  </main>
</template>

<script setup>
import { getBookDetail, toggleBookmark } from '@/api/book'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { BookmarkIcon, ArrowTopRightOnSquareIcon } from '@heroicons/vue/24/outline'
import { BookmarkIcon as BookmarkIconSolid } from '@heroicons/vue/24/solid'
import ThreeDimentionImage from '@/components/ThreeDimentionImage.vue'
import TradeCard from '@/components/TradeCard.vue'

const route = useRoute()

const book = ref({})

onMounted(async () => {
  const data = await getBookDetail(route.params.id)
  console.log(data)
  book.value = data
})

const handleBookmark = async (id) => {
  const response = await toggleBookmark(id)
  console.log(response.message)
  book.value.isBookmarked = response.isBookmarked
}
</script>
