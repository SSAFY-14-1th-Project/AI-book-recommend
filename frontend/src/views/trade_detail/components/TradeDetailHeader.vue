<template>
  <!-- ==================== 중고거래 상세 헤더 ==================== -->
  <div class="pb-6 mb-8 border-b border-base-content/10">
    <div class="flex justify-between items-start gap-4 flex-wrap">
      <!-- 왼쪽: 거래 기본 정보 -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-3 mb-4 flex-wrap">
          <h1 class="text-3xl font-bold text-base-content">{{ trade.title }}</h1>
          <span class="badge font-bold" :class="getStatusBadgeClass(trade.status)">
            {{ getStatusText(trade.status) }}
          </span>
          <span
            v-if="trade.saleType === 'free'"
            class="badge badge-success font-bold"
          >
            무료나눔
          </span>
        </div>

        <!-- 가격 및 할인율 -->
        <div class="flex items-baseline gap-3 mb-4">
          <div class="text-4xl font-bold text-primary">
            {{ formatPrice(trade.price, trade.saleType) }}
          </div>
          <!-- 할인율 표시 (무료나눔 제외) -->
          <div v-if="trade.saleType !== 'free' && getDiscountRate()" class="flex items-center gap-1">
            <span
              class="text-lg font-bold px-3 py-1 rounded"
              :class="getDiscountBadgeClass()"
            >
              {{ getDiscountRate() }}
            </span>
          </div>
        </div>

        <!-- 판매자 정보 & 지역 & 날짜 -->
        <div class="flex flex-wrap gap-4 text-base-content/70">
          <div class="flex items-center gap-2">
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
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            <span>{{ trade.user?.nickname || '익명' }}</span>
          </div>
          <span>·</span>
          <div class="flex items-center gap-2">
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
          </div>
          <span>·</span>
          <div class="flex items-center gap-2">
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
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>{{ formatDate(trade.createdAt) }}</span>
          </div>
          <span>·</span>
          <div class="flex items-center gap-2">
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
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
            <span>조회 {{ trade.viewCount || 0 }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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
// 가격 포맷팅
const formatPrice = (price, saleType) => {
  const type = saleType || props.trade.sale_type
  if (type === 'free') return '무료나눔'
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
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
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
  const bookPriceStandard = trade.book?.priceStandard || trade.book?.price_standard

  if (saleType === 'free' || !bookPriceStandard || bookPriceStandard === 0) {
    return null
  }

  if (!price || price === 0) {
    return null
  }

  const discountRate = ((bookPriceStandard - price) / bookPriceStandard) * 100
  const roundedRate = Math.round(discountRate * 10) / 10

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
  const bookPriceStandard = trade.book?.priceStandard || trade.book?.price_standard

  if (!price || !bookPriceStandard) return ''

  const discountRate = ((bookPriceStandard - price) / bookPriceStandard) * 100

  if (discountRate >= 50) {
    return 'bg-error text-error-content'
  } else if (discountRate >= 30) {
    return 'bg-warning text-warning-content'
  } else if (discountRate > 0) {
    return 'bg-success text-success-content'
  } else if (discountRate < 0) {
    return 'bg-base-300 text-base-content'
  }

  return 'bg-base-200 text-base-content'
}
</script>
