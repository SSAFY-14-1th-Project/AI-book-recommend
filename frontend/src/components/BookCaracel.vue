<template>
  <div class="relative bg-base-200 rounded-box px-6 py-3">
    <!-- 헤더 -->
    <div class="flex justify-between items-center mb-3">
      <div class="flex flex-col gap-1">
        <h3 class="text-xl font-bold text-base-content">{{ title }}</h3>
        <p class="text-sm">{{ description }}</p>
      </div>

      <!-- 커스텀 네비게이션 버튼 -->
      <div class="flex gap-2">
        <button
          ref="prevBtn"
          class="btn btn-circle btn-primary btn-sm hover:btn-primary-focus"
          aria-label="이전"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        <button
          ref="nextBtn"
          class="btn btn-circle btn-primary btn-sm hover:btn-primary-focus"
          aria-label="다음"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
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
    </div>

    <!-- Swiper 캐러셀 -->
    <Swiper
      :modules="modules"
      :slides-per-view="slidesPerView"
      :slides-per-group="slidesPerGroup"
      :space-between="spaceBetween"
      :loop="loop"
      :navigation="{
        prevEl: prevBtn,
        nextEl: nextBtn,
      }"
      :breakpoints="breakpoints"
      class="book-swiper"
      @swiper="onSwiper"
    >
      <!-- 로딩 상태 -->
      <template v-if="loading">
        <SwiperSlide v-for="_idx in 6">
          <BookCardSkeleton />
        </SwiperSlide>
      </template>

      <!-- 도서 슬라이드 -->
      <SwiperSlide v-for="book in props.books" :key="book.id" class="pt-3">
        <BookCard :book="book" :showRank="true" />
      </SwiperSlide>
    </Swiper>

    <!-- 페이지네이션 (선택사항) -->
    <div v-if="!loading && props.books.length > 0" class="flex justify-center mt-6 gap-2">
      <div class="swiper-pagination-custom"></div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="alert alert-error shadow-lg mt-4">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24"
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

    <!-- 데이터 없음 -->
    <div
      v-if="!loading && !error && props.books.length === 0"
      class="alert alert-info shadow-lg mt-4"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="h-6 w-6 shrink-0 stroke-current"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <span>베스트셀러 도서가 없습니다.</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

// Swiper 스타일 임포트
import 'swiper/css'
import 'swiper/css/navigation'
import BookCardSkeleton from './BookCardSkeleton.vue'
import BookCard from './BookCard.vue'

// Props 정의
const props = defineProps({
  // 도서 리스트
  books: {
    type: Array,
    required: true,
    default: () => [],
  },
  // 캐러셀 제목
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  // 로딩 상태
  loading: {
    type: Boolean,
    default: false,
  },
  // 에러 메시지
  error: {
    type: String,
    default: null,
  },
  // 화면당 표시할 슬라이드 수 (기본값)
  slidesPerView: {
    type: Number,
    default: 5,
  },
  // 한 번에 이동할 슬라이드 수
  slidesPerGroup: {
    type: Number,
    default: 3,
  },
  // 슬라이드 간 간격
  spaceBetween: {
    type: Number,
    default: 16,
  },
  // 무한 루프 여부
  loop: {
    type: Boolean,
    default: false,
  },
})

// Swiper 모듈
const modules = [Navigation]

// Swiper 인스턴스
const swiperInstance = ref(null)

// 네비게이션 버튼 ref
const prevBtn = ref(null)
const nextBtn = ref(null)

// 반응형 breakpoints
const breakpoints = computed(() => ({
  // 모바일
  320: {
    slidesPerView: 1,
    slidesPerGroup: 1,
    spaceBetween: 8,
  },
  // 작은 태블릿
  640: {
    slidesPerView: 2,
    slidesPerGroup: 2,
    spaceBetween: 12,
  },
  // 태블릿
  768: {
    slidesPerView: 3,
    slidesPerGroup: 3,
    spaceBetween: 16,
  },
  // 노트북
  1024: {
    slidesPerView: 4,
    slidesPerGroup: props.slidesPerGroup,
    spaceBetween: props.spaceBetween,
  },
  // 데스크톱
  1280: {
    slidesPerView: props.slidesPerView,
    slidesPerGroup: props.slidesPerGroup,
    spaceBetween: props.spaceBetween,
  },
  // 큰 화면
  1536: {
    slidesPerView: props.slidesPerView + 1,
    slidesPerGroup: props.slidesPerGroup + 1,
    spaceBetween: 20,
  },
}))

// Swiper 인스턴스 저장
function onSwiper(swiper) {
  swiperInstance.value = swiper
}

// 이미지 로드 에러 처리
function handleImageError(event) {
  event.target.src = '/placeholder-book.png'
}
</script>

<style scoped>
/* 스켈레톤 로딩 애니메이션 */
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 이미지 렌더링 품질 개선 */
img {
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
}
</style>
