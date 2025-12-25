<template>
  <!-- ==================== 도서 검색 입력 ==================== -->
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
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
        거래할 도서 선택
        <span class="text-error text-sm">*</span>
      </h3>

      <!-- 선택된 도서가 없을 때: 검색창 표시 -->
      <div v-if="!selectedBook" class="space-y-3">
        <div class="relative">
          <div class="relative">
            <input
              v-model="searchQuery"
              @input="onSearch"
              @focus="showDropdown = true"
              type="text"
              placeholder="도서명을 입력하여 검색하세요..."
              class="input input-bordered w-full pr-10"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 absolute right-3 top-1/2 -translate-y-1/2 text-base-content/40"
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
          </div>

          <!-- 검색 결과 드롭다운 -->
          <ul
            v-if="showDropdown && searchResults.length > 0"
            class="absolute z-10 w-full bg-base-100 border border-base-content/10 rounded-lg mt-2 max-h-80 overflow-y-auto shadow-xl"
          >
            <li
              v-for="book in searchResults"
              :key="book.id"
              @click="selectBook(book)"
              class="p-4 hover:bg-base-200 cursor-pointer border-b border-base-content/5 last:border-b-0 transition-colors"
            >
              <div class="flex gap-3">
                <img
                  :src="book.cover || '/placeholder-book.png'"
                  :alt="book.title"
                  class="w-12 h-16 object-cover rounded shadow-sm"
                  @error="(e) => (e.target.src = '/placeholder-book.png')"
                />
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-sm line-clamp-1">{{ book.title }}</p>
                  <p class="text-xs text-base-content/60 mt-1">{{ book.author }}</p>
                  <div class="flex gap-2 mt-2">
                    <span v-if="book.category" class="badge badge-primary badge-xs">
                      {{ book.category.name }}
                    </span>
                    <span v-if="book.price_standard" class="text-xs text-base-content/50">
                      정가 {{ book.price_standard.toLocaleString() }}원
                    </span>
                  </div>
                </div>
              </div>
            </li>
          </ul>

          <!-- 검색 결과 없음 -->
          <div
            v-if="showDropdown && searchQuery.length >= 2 && searchResults.length === 0"
            class="absolute z-10 w-full bg-base-100 border border-base-content/10 rounded-lg mt-2 p-6 text-center shadow-xl"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-12 w-12 mx-auto text-base-content/20 mb-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p class="text-sm text-base-content/50">검색 결과가 없습니다</p>
          </div>
        </div>

        <p class="text-xs text-base-content/60 flex items-center gap-1">
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
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          최소 2자 이상 입력하면 자동으로 검색됩니다
        </p>
      </div>

      <!-- 선택된 도서 표시 -->
      <div v-else class="space-y-3">
        <div
          class="bg-gradient-to-br from-primary/5 to-secondary/5 rounded-lg p-4 border border-primary/20"
        >
          <div class="flex gap-4">
            <img
              :src="selectedBook.cover || '/placeholder-book.png'"
              :alt="selectedBook.title"
              class="w-20 h-28 object-cover rounded-lg shadow-md"
              @error="(e) => (e.target.src = '/placeholder-book.png')"
            />
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start gap-2">
                <div class="flex-1 min-w-0">
                  <p class="font-bold text-base line-clamp-2 leading-tight">
                    {{ selectedBook.title }}
                  </p>
                  <p class="text-sm text-base-content/70 mt-1">{{ selectedBook.author }}</p>
                </div>
                <button
                  type="button"
                  @click="clearSelection"
                  class="btn btn-ghost btn-sm btn-circle"
                  title="선택 취소"
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
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              <div class="flex flex-wrap gap-2 mt-3">
                <span v-if="selectedBook.category" class="badge badge-primary badge-sm">
                  {{ selectedBook.category.name }}
                </span>
                <span v-if="selectedBook.price_standard" class="badge badge-outline badge-sm">
                  정가 {{ selectedBook.price_standard.toLocaleString() }}원
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// ==================== Props & Emits ====================
const props = defineProps({
  modelValue: {
    type: Object,
    default: null,
  },
  searchResults: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue', 'search'])

// ==================== 상태 관리 ====================
const searchQuery = ref('')
const showDropdown = ref(false)

// ==================== Computed ====================
const selectedBook = ref(props.modelValue)

// ==================== Methods ====================
const onSearch = () => {
  emit('search', searchQuery.value)
}

const selectBook = (book) => {
  selectedBook.value = book
  emit('update:modelValue', book)
  searchQuery.value = ''
  showDropdown.value = false
}

const clearSelection = () => {
  selectedBook.value = null
  emit('update:modelValue', null)
}

// 외부 클릭 시 드롭다운 닫기
document.addEventListener('click', (e) => {
  if (!e.target.closest('.relative')) {
    showDropdown.value = false
  }
})
</script>
