<template>
  <!-- ==================== 가격 및 거래 정보 ==================== -->
  <div class="card bg-base-100 shadow-sm border border-base-content/5">
    <div class="card-body p-6">
      <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-primary"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"
          />
        </svg>
        거래 정보
      </h3>

      <div class="space-y-5">
        <!-- 판매 유형 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">판매 유형</span>
          </label>
          <div class="grid grid-cols-2 gap-3">
            <label
              class="relative cursor-pointer"
              :class="{ 'opacity-50': saleType === 'free' }"
            >
              <input
                type="radio"
                :checked="saleType === 'sale'"
                @change="$emit('update:saleType', 'sale')"
                class="radio radio-primary absolute opacity-0"
              />
              <div
                class="border-2 rounded-lg p-4 text-center transition-all hover:border-primary/50"
                :class="
                  saleType === 'sale'
                    ? 'border-primary bg-primary/5'
                    : 'border-base-content/10'
                "
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-8 w-8 mx-auto mb-2"
                  :class="saleType === 'sale' ? 'text-primary' : 'text-base-content/40'"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p class="font-semibold text-sm">판매</p>
              </div>
            </label>

            <label
              class="relative cursor-pointer"
              :class="{ 'opacity-50': saleType === 'sale' }"
            >
              <input
                type="radio"
                :checked="saleType === 'free'"
                @change="$emit('update:saleType', 'free')"
                class="radio radio-primary absolute opacity-0"
              />
              <div
                class="border-2 rounded-lg p-4 text-center transition-all hover:border-primary/50"
                :class="
                  saleType === 'free'
                    ? 'border-primary bg-primary/5'
                    : 'border-base-content/10'
                "
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-8 w-8 mx-auto mb-2"
                  :class="saleType === 'free' ? 'text-primary' : 'text-base-content/40'"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"
                  />
                </svg>
                <p class="font-semibold text-sm">무료나눔</p>
              </div>
            </label>
          </div>
        </div>

        <!-- 가격 (판매 선택 시만 표시) -->
        <div v-if="saleType === 'sale'" class="form-control">
          <label class="label">
            <span class="label-text font-medium">판매 가격</span>
            <span v-if="bookPriceStandard" class="label-text-alt text-primary font-semibold">
              도서 정가: {{ bookPriceStandard.toLocaleString() }}원
            </span>
          </label>
          <label class="input-group">
            <input
              :value="price"
              @input="$emit('update:price', Number($event.target.value))"
              type="number"
              min="0"
              step="1000"
              placeholder="0"
              class="input input-bordered w-full focus:input-primary"
            />
            <span class="bg-base-200">원</span>
          </label>
          <label class="label">
            <span class="label-text-alt text-base-content/50">
              {{ price > 0 ? price.toLocaleString() + '원' : '가격을 입력하세요' }}
            </span>
            <span v-if="bookPriceStandard && price > 0" class="label-text-alt">
              <span v-if="price < bookPriceStandard" class="text-success font-semibold">
                {{ Math.round(((bookPriceStandard - price) / bookPriceStandard) * 100) }}% 할인
              </span>
              <span v-else-if="price > bookPriceStandard" class="text-warning">
                정가보다 {{ Math.round(((price - bookPriceStandard) / bookPriceStandard) * 100) }}% 높음
              </span>
              <span v-else class="text-base-content/50">정가와 동일</span>
            </span>
          </label>
        </div>

        <!-- 거래 지역 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">거래 희망 지역</span>
          </label>
          <select
            :value="region"
            @change="$emit('update:region', $event.target.value)"
            class="select select-bordered w-full focus:select-primary"
          >
            <option value="all">🌏 전국</option>
            <optgroup label="특별시/광역시">
              <option value="seoul">🏙️ 서울특별시</option>
              <option value="busan">🌊 부산광역시</option>
              <option value="daegu">🏔️ 대구광역시</option>
              <option value="incheon">✈️ 인천광역시</option>
              <option value="gwangju">🌳 광주광역시</option>
              <option value="daejeon">🔬 대전광역시</option>
              <option value="ulsan">🏭 울산광역시</option>
              <option value="sejong">🏛️ 세종특별자치시</option>
            </optgroup>
            <optgroup label="도">
              <option value="gyeonggi">🏘️ 경기도</option>
              <option value="gangwon">⛰️ 강원특별자치도</option>
              <option value="chungbuk">🌾 충청북도</option>
              <option value="chungnam">🌊 충청남도</option>
              <option value="jeonbuk">🌾 전라북도</option>
              <option value="jeonnam">🌊 전라남도</option>
              <option value="gyeongbuk">⛰️ 경상북도</option>
              <option value="gyeongnam">🏖️ 경상남도</option>
              <option value="jeju">🏝️ 제주특별자치도</option>
            </optgroup>
          </select>
        </div>

        <!-- 카카오톡 오픈채팅 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">카카오톡 오픈채팅 링크</span>
            <span class="label-text-alt text-base-content/50">선택사항</span>
          </label>
          <div class="relative">
            <input
              :value="kakaoChatUrl"
              @input="$emit('update:kakaoChatUrl', $event.target.value)"
              type="url"
              placeholder="https://open.kakao.com/o/..."
              class="input input-bordered w-full pl-10 focus:input-primary"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 absolute left-3 top-1/2 -translate-y-1/2 text-base-content/40"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
          </div>
          <label class="label">
            <span class="label-text-alt text-base-content/50 text-xs leading-relaxed">
              💡 카카오톡 → 채팅 → + → 오픈채팅 → 1:1 채팅 만들기 → 링크 복사
            </span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props & Emits ====================
defineProps({
  saleType: {
    type: String,
    required: true,
  },
  price: {
    type: Number,
    required: true,
  },
  region: {
    type: String,
    required: true,
  },
  kakaoChatUrl: {
    type: String,
    default: '',
  },
  bookPriceStandard: {
    type: Number,
    default: null,
  },
})

defineEmits(['update:saleType', 'update:price', 'update:region', 'update:kakaoChatUrl'])
</script>
