<template>
  <!-- ==================== 중고거래 카드 ==================== -->
  <RouterLink
    :to="{ name: 'tradeDetail', params: { id: trade.id } }"
    class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 cursor-pointer h-full flex flex-col"
  >
    <!-- 거래 이미지 영역 -->
    <figure class="bg-base-200 overflow-hidden relative">
      <img
        v-if="trade.image"
        :src="getImageUrl(trade.image)"
        :alt="trade.title"
        class="w-full h-48 object-cover"
        loading="lazy"
        @error="handleImageError"
      />
      <!-- 기본 이미지 -->
      <div v-else class="w-full h-48 flex items-center justify-center text-base-content/30">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-20 w-20"
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
      </div>

      <!-- 거래 상태 배지 -->
      <div class="absolute top-2 left-2 z-10">
        <span class="badge font-bold" :class="getStatusBadgeClass(trade.status)">
          {{ getStatusText(trade.status) }}
        </span>
      </div>

      <!-- 거래 타입 배지 (무료나눔) -->
      <div v-if="trade.saleType === 'free'" class="absolute top-2 right-2 z-10">
        <span class="badge badge-success font-bold">무료나눔</span>
      </div>
    </figure>

    <!-- 거래 정보 영역 -->
    <div class="card-body p-4">
      <!-- 거래 제목 -->
      <h4 class="card-title text-sm line-clamp-2 min-h-10">
        {{ trade.title }}
      </h4>
      <!-- 거래 도서 제목 -->
      <h4 class="card-title text-sm line-clamp-2 min-h-10">
        {{ trade.bookTitle }}
      </h4>

      <!-- 가격 -->
      <div class="flex items-center gap-2">
        <div class="text-lg font-bold text-primary">
          {{ formatPrice(trade.price, trade.saleType) }}
        </div>
        <!-- 할인율 표시 (무료나눔 제외) -->
        <div v-if="trade.saleType !== 'free' && getDiscountRate()" class="flex items-center gap-1">
          <span
            class="text-xs font-bold px-2 py-1 rounded"
            :class="getDiscountBadgeClass()"
          >
            {{ getDiscountRate() }}
          </span>
        </div>
      </div>

      <!-- 지역 및 날짜 -->
      <div class="flex items-center gap-2 text-xs text-base-content/70">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        <span>{{ getRegionText(trade.region) }}</span>
        <span>·</span>
        <span>{{ formatDate(trade.createdAt) }}</span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

// ==================== Props ====================
const props = defineProps({
  trade: {
    type: Object,
    required: true,
  },
})

// ==================== 지역 매핑 ====================
const regionMap = {
  seoul: '서울',
  busan: '부산',
  daegu: '대구',
  incheon: '인천',
  gwangju: '광주',
  daejeon: '대전',
  ulsan: '울산',
  sejong: '세종',
  gyeonggi: '경기',
  gangwon: '강원',
  chungbuk: '충북',
  chungnam: '충남',
  jeonbuk: '전북',
  jeonnam: '전남',
  gyeongbuk: '경북',
  gyeongnam: '경남',
  jeju: '제주',
}

// ==================== Methods ====================
// 이미지 URL 가져오기
const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `http://localhost:8000${imagePath}`
}

// 가격 포맷팅
const formatPrice = (price, saleType) => {
  if (saleType === 'free') return '무료나눔'
  if (!price) return '가격 미정'
  return `${price.toLocaleString()}원`
}

// 지역 텍스트
const getRegionText = (region) => {
  return regionMap[region] || region || '지역 미정'
}

// 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '오늘'
  if (days === 1) return '어제'
  if (days < 7) return `${days}일 전`
  return date.toLocaleDateString('ko-KR')
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

// 상태 배지 클래스
const getStatusBadgeClass = (status) => {
  const classMap = {
    available: 'badge-success',
    reserved: 'badge-warning',
    sold: 'badge-ghost',
  }
  return classMap[status] || ''
}

// 할인율 계산
const getDiscountRate = () => {
  const trade = props.trade
  const price = trade.price
  const saleType = trade.saleType || trade.sale_type
  // camelCase와 snake_case 둘 다 지원
  const bookPriceStandard = trade.bookPriceStandard || trade.book_price_standard

  // 무료나눔이거나 정가가 없으면 null 반환
  if (saleType === 'free' || !bookPriceStandard || bookPriceStandard === 0) {
    return null
  }

  // 중고가격이 없으면 null 반환
  if (!price || price === 0) {
    return null
  }

  // 할인율 계산: ((정가 - 중고가) / 정가) * 100
  const discountRate = ((bookPriceStandard - price) / bookPriceStandard) * 100

  // 소수점 첫째자리까지 표시
  const roundedRate = Math.round(discountRate * 10) / 10

  // 할인이면 -%, 오히려 비싸면 +%
  if (roundedRate > 0) {
    return `-${roundedRate}%`
  } else if (roundedRate < 0) {
    return `+${Math.abs(roundedRate)}%`
  }

  return null
}

// 할인율 배지 색상 클래스
const getDiscountBadgeClass = () => {
  const trade = props.trade
  const price = trade.price
  // camelCase와 snake_case 둘 다 지원
  const bookPriceStandard = trade.bookPriceStandard || trade.book_price_standard

  if (!price || !bookPriceStandard) return ''

  const discountRate = ((bookPriceStandard - price) / bookPriceStandard) * 100

  // 할인율에 따라 색상 변경
  if (discountRate >= 50) {
    // 50% 이상 할인: 빨간색 (매우 저렴)
    return 'bg-error text-error-content'
  } else if (discountRate >= 30) {
    // 30% 이상 할인: 주황색 (저렴)
    return 'bg-warning text-warning-content'
  } else if (discountRate > 0) {
    // 할인: 초록색
    return 'bg-success text-success-content'
  } else if (discountRate < 0) {
    // 정가보다 비쌈: 회색
    return 'bg-base-300 text-base-content'
  }

  return 'bg-base-200 text-base-content'
}

// 이미지 로드 실패 시 처리
const handleImageError = (event) => {
  event.target.style.display = 'none'
}
</script>

<style scoped>
/* 텍스트 2줄 말줄임 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
