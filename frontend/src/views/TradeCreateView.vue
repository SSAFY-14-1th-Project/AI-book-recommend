<template>
  <div class="trade-create container mx-auto p-4 max-w-2xl">
    <h1 class="text-2xl font-bold mb-6">중고거래 등록</h1>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- 도서 선택 -->
      <div class="form-control">
        <label class="label">
          <span class="label-text">도서 선택 *</span>
        </label>
        <div class="relative">
          <input
            v-model="bookSearch"
            @input="searchBooks"
            @focus="showDropdown = true"
            type="text"
            placeholder="도서명을 검색하세요..."
            class="input input-bordered w-full"
          />
          <!-- 자동완성 드롭다운 -->
          <!-- 여기서 지금 책 제목밖에 안나오는 점이 아쉽다. 옆에 저자도 뜨면 괜찮을 듯 -->
          <ul
            v-if="showDropdown && bookResults.length > 0"
            class="absolute z-10 w-full bg-base-100 border border-base-300 rounded-lg mt-1 max-h-60 overflow-y-auto shadow-lg"
          >
            <li
              v-for="book in bookResults"
              :key="book.id"
              @click="selectBook(book)"
              class="p-3 hover:bg-base-200 cursor-pointer border-b last:border-b-0"
            >
              <p class="font-medium">{{ book.title }}</p>
              <p class="text-sm text-gray-500">{{ book.author }}</p>
            </li>
          </ul>
        </div>
        <!-- 선택된 도서 표시 -->
        <!-- 이게 지금 폼 밑에 존재하는데 저 검색창에 집어넣는건 불가능하려나.. -->
        <div v-if="selectedBook" class="mt-2 p-3 bg-base-200 rounded-lg flex justify-between items-center">
          <div>
            <p class="font-medium">{{ selectedBook.title }}</p>
            <p class="text-sm text-gray-500">{{ selectedBook.author }}</p>
          </div>
          <button type="button" @click="clearBook" class="btn btn-ghost btn-sm">✕</button>
        </div>
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
        <!-- v-model.number => 숫자로 변환해서 값을 집어넣어줌 -->
        <input
          v-model.number="form.price"
          type="number"
          min="0"
          placeholder="가격을 입력하세요"
          class="input input-bordered w-full"
        />
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
        <!-- 여기서 url 정보를 어떻게 불러왔길래 유효성 검사가 된거지.. 여긴 좀 이해가 안간다.. -->
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
        <!-- image/ → MIME 타입 -->
        <!-- * → 모든 이미지 타입 -->
        <!-- gif도 가능함 ㄷㄷ -->
        <input
          type="file"
          @change="handleImageUpload"
          accept="image/*"
          class="file-input file-input-bordered w-full"
        />
        <!-- 이미지 미리보기 -->
        <div v-if="imagePreview" class="mt-2">
          <img :src="imagePreview" alt="미리보기" class="w-32 h-32 object-cover rounded-lg" />
        </div>
      </div>

      <!-- 제출 버튼 -->
      <div class="flex gap-2 pt-4">
        <button type="submit" class="btn btn-primary flex-1" :disabled="!selectedBook">
          등록하기
        </button>
        <button type="button" @click="router.back()" class="btn btn-ghost">
          취소
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createTrade } from '@/api/trades'
import client from '@/api/client'

const router = useRouter()

// 폼 데이터
const form = reactive({
  title: '',
  content: '',
  saleType: 'sale',
  price: 0,
  region: 'seoul',
  kakaoChatUrl: '',
  image: null
})

// 도서 검색 관련
const bookSearch = ref('')
const bookResults = ref([])
const selectedBook = ref(null)
const showDropdown = ref(false)

// 이미지 미리보기
const imagePreview = ref(null)

// 도서 검색 (자동완성)
// 1. 사용자가 검색창에 글자를 입력한다
// 2. 이전에 예약된 검색 요청을 취소한다
// 3. 300ms 동안 추가 입력이 없으면
// 4. 입력 글자가 2자 이상일 때만
// 5. 서버(/api/books/autocomplete/)에 검색 요청
// 6. 결과를 자동완성 목록에 표시
let searchTimeout = null
const searchBooks = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    if (bookSearch.value.length < 2) {
      bookResults.value = []
      return
    }
    try {
      // 실제 요청 url: /api/books/autocomplete/?q=입력갑
      // params → query string 전용
      // DRF 쪽에서 request.query_params['q'] 로 받음
      const response = await client.get('/api/books/autocomplete/', {
        params: { q: bookSearch.value }
      })
      // 템플릿에 자동완성 리스트 즉시 갱신
      bookResults.value = response.data
    } catch (error) {
      console.error('도서 검색 실패:', error)
    }
  }, 300)
}

// 도서 선택
const selectBook = (book) => {
  selectedBook.value = book
  bookSearch.value = ''
  bookResults.value = []
  showDropdown.value = false
}

// 도서 선택 취소
const clearBook = () => {
  selectedBook.value = null
}

// 이미지 업로드 처리
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // File 객체 그대로 state에 저장 (django/drf로 보낼 때 FormData에 넣기 위함)
    form.image = file
    // 미리보기 생성 (미리보기 용으로만 base64 변환)
    // <img :src="imagePreview" /> 용도
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 폼 제출
// 도서 선택 여부 검증
// FormData 생성
// 텍스트 필드 append
// 조건부 필드 append (URL, 이미지)
// API 호출
// 성공 → 알림 + 라우팅
const handleSubmit = async () => {
  // ✅ 자동완성 + 선택 구조에서 필수
  // ✅ 서버로 쓸데없는 요청 안 보냄
  if (!selectedBook.value) {
    alert('도서를 선택해주세요.')
    return
  }

  try {
    // formData : File 때문에 필수
    // multipart/form-data
    // DRF ImageField, FileField와 100% 호환
    const formData = new FormData()
    formData.append('title', form.title)
    formData.append('content', form.content)
    formData.append('sale_type', form.saleType)
    formData.append('price', form.saleType === 'free' ? 0 : form.price)
    formData.append('region', form.region)
    if (form.kakaoChatUrl) {
      formData.append('kakao_chat_url', form.kakaoChatUrl)
    }
    if (form.image) {
      formData.append('image', form.image)
    }

    await createTrade(selectedBook.value.id, formData)
    alert('게시글이 등록되었습니다.')
    router.push({ name: 'trade-list' })
  } catch (error) {
    console.error('게시글 등록 실패:', error)
    // DRF serializer 에러 그대로 확인 가능
    // 개발 단계에서 매우 유용
    if (error.response?.data) {
      // 메세지가 좀 맘에 안들어서 평탄화로 정상화 작업 했습니다.
      // 궁금하시다면 카카오톡 url에 https://www.naver.com 과 같은 형식으로
      // 값을 입력 해보세요!
      // alert(JSON.stringify(error.response.data))
      const errors = error.response.data
      const message = Object.values(errors)
        .flat()
        .join('\n')
      alert(message)
    } else {
      alert('게시글 등록에 실패했습니다.')
    }
  }
}

// 드롭다운 외부 클릭 시 닫기
document.addEventListener('click', (e) => {
  if (!e.target.closest('.relative')) {
    showDropdown.value = false
  }
})
</script>
