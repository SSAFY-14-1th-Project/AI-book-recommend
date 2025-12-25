<template>
  <!-- ==================== 이미지 업로드 ==================== -->
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
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        상품 이미지
        <span class="label-text-alt text-base-content/50 font-normal ml-auto">선택사항</span>
      </h3>

      <!-- 이미지 미리보기 영역 -->
      <div class="space-y-4">
        <!-- 이미지가 없을 때 -->
        <div v-if="!imagePreview" class="relative">
          <input
            ref="fileInput"
            type="file"
            @change="handleImageChange"
            accept="image/*"
            class="file-input file-input-bordered w-full focus:file-input-primary"
          />
          <div class="mt-3 p-6 border-2 border-dashed border-base-content/10 rounded-lg bg-base-200/30">
            <div class="text-center text-base-content/50">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-12 w-12 mx-auto mb-3 text-base-content/20"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <p class="text-sm font-medium mb-1">책 사진을 등록해주세요</p>
              <p class="text-xs">JPG, PNG, GIF 파일 업로드 가능 (최대 5MB)</p>
            </div>
          </div>
        </div>

        <!-- 이미지 미리보기 -->
        <div v-else class="space-y-3">
          <div class="relative rounded-lg overflow-hidden border border-base-content/10 bg-base-200/50">
            <!-- 이미지 -->
            <div class="aspect-video flex items-center justify-center bg-base-300/30">
              <img
                :src="imagePreview"
                alt="미리보기"
                class="max-w-full max-h-full object-contain"
              />
            </div>

            <!-- 삭제 버튼 -->
            <button
              type="button"
              @click="removeImage"
              class="absolute top-3 right-3 btn btn-circle btn-sm bg-base-100/90 hover:bg-error hover:text-error-content border-base-content/10"
              title="이미지 삭제"
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

          <!-- 다시 선택 버튼 -->
          <button
            type="button"
            @click="$refs.fileInput.click()"
            class="btn btn-outline btn-sm w-full"
          >
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
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            다른 이미지 선택
          </button>
          <input
            ref="fileInput"
            type="file"
            @change="handleImageChange"
            accept="image/*"
            class="hidden"
          />
        </div>

        <!-- 안내 메시지 -->
        <div class="alert alert-info shadow-sm">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 shrink-0"
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
          <div class="text-xs">
            <p class="font-semibold">📸 사진 촬영 팁</p>
            <ul class="mt-1 space-y-0.5 text-base-content/70">
              <li>• 책의 전체적인 모습이 잘 보이도록 촬영해주세요</li>
              <li>• 밝은 곳에서 촬영하면 더 좋습니다</li>
              <li>• 책의 상태가 명확하게 보이도록 해주세요</li>
            </ul>
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
    type: File,
    default: null,
  },
  preview: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'update:preview'])

// ==================== 상태 관리 ====================
const fileInput = ref(null)
const imagePreview = ref(props.preview)

// ==================== Methods ====================
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 파일 크기 검증 (5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('이미지 파일 크기는 5MB를 초과할 수 없습니다.')
    return
  }

  // 파일 타입 검증
  if (!file.type.startsWith('image/')) {
    alert('이미지 파일만 업로드 가능합니다.')
    return
  }

  // File 객체 전달
  emit('update:modelValue', file)

  // 미리보기 생성
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    emit('update:preview', e.target.result)
  }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  imagePreview.value = null
  emit('update:modelValue', null)
  emit('update:preview', null)
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>
