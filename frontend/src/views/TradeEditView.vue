<template>
  <div class="trade-edit container mx-auto p-4 max-w-2xl">
    <h1 class="text-2xl font-bold mb-6">중고거래 수정</h1>

    <div v-if="loading" class="text-center py-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-4">
      <!-- 도서 정보 (수정 불가) -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">도서 정보</span>
        </label>
        <div class="p-3 bg-base-200 rounded-lg">
          <p class="font-medium">{{ trade?.book?.title }}</p>
          <p class="text-sm text-gray-500">{{ trade?.book?.author }}</p>
        </div>
        <label class="label">
          <span class="label-text-alt text-gray-500">도서는 수정할 수 없습니다</span>
        </label>
      </div>

      <!-- 제목 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">제목 *</span>
        </label>
        <input
          v-model="form.title"
          type="text"
          placeholder="제목을 입력하세요"
          class="input input-bordered w-full"
          required
        />
      </div>

      <!-- 내용 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">내용 *</span>
        </label>
        <textarea
          v-model="form.content"
          placeholder="상품 설명을 입력하세요"
          class="textarea textarea-bordered h-32"
          required
        ></textarea>
      </div>

      <!-- 판매유형 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">판매유형</span>
        </label>
        <select v-model="form.saleType" class="select select-bordered w-full">
          <option value="sale">판매</option>
          <option value="free">무료나눔</option>
        </select>
      </div>

      <!-- 가격 -->
      <div v-if="form.saleType === 'sale'" class="form-control">
        <label class="label">
          <span class="label-text">가격</span>
        </label>
        <input
          v-model.number="form.price"
          type="number"
          min="0"
          placeholder="가격을 입력하세요"
          class="input input-bordered w-full"
        />
      </div>

      <!-- 거래 상태 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">거래 상태</span>
        </label>
        <select v-model="form.status" class="select select-bordered w-full">
          <option value="available">판매중</option>
          <option value="reserved">예약중</option>
          <option value="sold">판매완료</option>
        </select>
      </div>

      <!-- 지역 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">거래 지역</span>
        </label>
        <select v-model="form.region" class="select select-bordered w-full">
          <option value="all">전국</option>
          <option value="seoul">서울특별시</option>
          <option value="busan">부산광역시</option>
          <option value="daegu">대구광역시</option>
          <option value="incheon">인천광역시</option>
          <option value="gwangju">광주광역시</option>
          <option value="daejeon">대전광역시</option>
          <option value="ulsan">울산광역시</option>
          <option value="sejong">세종특별자치시</option>
          <option value="gyeonggi">경기도</option>
          <option value="gangwon">강원특별자치도</option>
          <option value="chungbuk">충청북도</option>
          <option value="chungnam">충청남도</option>
          <option value="jeonbuk">전라북도</option>
          <option value="jeonnam">전라남도</option>
          <option value="gyeongbuk">경상북도</option>
          <option value="gyeongnam">경상남도</option>
          <option value="jeju">제주특별자치도</option>
        </select>
      </div>

      <!-- 카카오톡 오픈채팅 URL -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">카카오톡 오픈채팅 링크</span>
        </label>
        <input
          v-model="form.kakaoChatUrl"
          type="url"
          placeholder="https://open.kakao.com/o/..."
          class="input input-bordered w-full"
        />
        <label class="label">
          <span class="label-text-alt text-gray-500">
            카카오톡 → 채팅 → + → 오픈채팅 → 1:1 채팅 → 프로필 설정 → 링크 복사
          </span>
        </label>
      </div>

      <!-- 이미지 업로드 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">상품 이미지</span>
        </label>
        <!-- 현재 이미지 표시 -->
        <div v-if="currentImage && !imagePreview" class="mb-2">
          <p class="text-sm text-gray-500 mb-1">현재 이미지:</p>
          <img :src="currentImage" alt="현재 이미지" class="w-32 h-32 object-cover rounded-lg" />
        </div>
        <input
          type="file"
          @change="handleImageUpload"
          accept="image/*"
          class="file-input file-input-bordered w-full"
        />
        <!-- 새 이미지 미리보기 -->
        <div v-if="imagePreview" class="mt-2">
          <p class="text-sm text-gray-500 mb-1">새 이미지:</p>
          <img :src="imagePreview" alt="미리보기" class="w-32 h-32 object-cover rounded-lg" />
        </div>
      </div>

      <!-- 제출 버튼 -->
      <div class="flex gap-2 pt-4">
        <button type="submit" class="btn btn-primary flex-1">
          수정하기
        </button>
        <button type="button" @click="router.back()" class="btn btn-ghost">
          취소
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// import { getTradeDetail, updateTrade } from '@/api/trades'
import { getTradeForEdit, updateTrade } from '@/api/trades'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const trade = ref(null)

// 폼 데이터
const form = reactive({
  title: '',
  content: '',
  saleType: 'sale',
  price: 0,
  status: 'available',
  region: 'seoul',
  kakaoChatUrl: '',
  image: null
})

// 이미지 관련
const currentImage = ref(null)
const imagePreview = ref(null)

// 기존 데이터 불러오기
onMounted(async () => {
  try {
    const { id } = route.params
    // const response = await getTradeDetail(id)
    const response = await getTradeForEdit(id)
    trade.value = response.data

    // 폼에 기존 데이터 채우기
    form.title = trade.value.title
    form.content = trade.value.content
    form.saleType = trade.value.saleType
    form.price = trade.value.price
    form.status = trade.value.status
    form.region = trade.value.region
    form.kakaoChatUrl = trade.value.kakaoChatUrl || ''

    // 현재 이미지 URL 저장
    if (trade.value.image) {
      currentImage.value = trade.value.image.startsWith('http')
        ? trade.value.image
        : `http://localhost:8000${trade.value.image}`
    }
  } catch (error) {
    console.error('데이터 불러오기 실패:', error)
    alert('게시글을 불러올 수 없습니다.')
    router.back()
  } finally {
    loading.value = false
  }
})

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    form.image = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 폼 제출
const handleSubmit = async () => {
  try {
    const formData = new FormData()
    formData.append('title', form.title)
    formData.append('content', form.content)
    formData.append('sale_type', form.saleType)
    formData.append('price', form.saleType === 'free' ? 0 : form.price)
    formData.append('status', form.status)
    formData.append('region', form.region)

    if (form.kakaoChatUrl) {
      formData.append('kakao_chat_url', form.kakaoChatUrl)
    }
    if (form.image) {
      formData.append('image', form.image)
    }

    await updateTrade(trade.value.id, formData)
    alert('게시글이 수정되었습니다.')
    router.push({ name: 'trade-detail', params: { id: trade.value.id } })
  } catch (error) {
    console.error('게시글 수정 실패:', error)
    if (error.response?.data) {
      const errors = error.response.data
      const message = Object.values(errors)
        .flat()
        .join('\n')
      alert(message)
    } else {
      alert('게시글 수정에 실패했습니다.')
    }
  }
}
</script>
