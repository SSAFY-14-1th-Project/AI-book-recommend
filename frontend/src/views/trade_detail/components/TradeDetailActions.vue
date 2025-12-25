<template>
  <!-- ==================== 중고거래 액션 버튼 ==================== -->
  <div class="flex flex-col gap-4 sticky top-8">
    <!-- 본인 게시글이 아닐 때: 채팅하기 버튼 -->
    <div v-if="!isOwner && kakaoChatUrl" class="space-y-4">
      <a
        :href="kakaoChatUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="btn btn-primary btn-lg w-full"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 mr-2"
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
        카카오톡 오픈채팅으로 연락하기
      </a>
      <div class="text-sm text-base-content/60 text-center">
        안전한 거래를 위해 직거래를 권장합니다
      </div>
    </div>

    <!-- 본인 게시글일 때: 수정/삭제 버튼 -->
    <div v-if="isOwner" class="space-y-3">
      <RouterLink :to="{ name: 'tradeEdit', params: { id: tradeId } }" class="btn btn-outline btn-lg w-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
          />
        </svg>
        수정하기
      </RouterLink>
      <button @click="emit('delete')" class="btn btn-error btn-lg w-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
          />
        </svg>
        삭제하기
      </button>
    </div>

    <!-- 목록으로 버튼 (항상 표시) -->
    <RouterLink :to="{ name: 'trade' }" class="btn btn-ghost btn-lg w-full">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5 mr-2"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 10h16M4 14h16M4 18h16"
        />
      </svg>
      목록으로 돌아가기
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

// ==================== Props ====================
defineProps({
  tradeId: {
    type: Number,
    required: true,
  },
  isOwner: {
    type: Boolean,
    default: false,
  },
  kakaoChatUrl: {
    type: String,
    default: '',
  },
})

// ==================== Emits ====================
const emit = defineEmits(['delete'])
</script>
