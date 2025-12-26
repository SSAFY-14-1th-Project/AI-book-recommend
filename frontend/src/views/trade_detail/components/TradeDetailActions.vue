<template>
  <!-- ==================== 중고거래 액션 버튼 ==================== -->
  <div class="flex flex-col gap-4 sticky top-8">
    <!-- 본인 게시글이 아닐 때: 채팅하기 버튼 (판매완료 시 숨김, 로그인 필요) -->
    <div v-if="!isOwner && kakaoChatUrl && props.status !== 'sold' && props.isLoggedIn" class="space-y-4">
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

    <!-- 비로그인 사용자: 로그인 안내 메시지 -->
    <div v-if="!isOwner && !props.isLoggedIn && props.status !== 'sold'" class="space-y-4">
      <div class="alert alert-warning">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
        <div class="flex flex-col gap-1">
          <span class="font-semibold">로그인이 필요합니다.</span>
          <span class="text-sm">판매자와 연락하려면 로그인해주세요.</span>
        </div>
      </div>
      <RouterLink :to="{ name: 'login' }" class="btn btn-primary btn-lg w-full">
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
            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
          />
        </svg>
        로그인하기
      </RouterLink>
    </div>

    <!-- 본인 게시글이 아니고 판매완료된 경우: 안내 메시지 -->
    <div v-if="!isOwner && props.status === 'sold'" class="space-y-4">
      <div class="alert alert-info">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 shrink-0"
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
        <span>판매가 완료된 상품입니다.</span>
      </div>
    </div>

    <!-- 본인 게시글일 때: 수정/삭제 버튼 -->
    <div v-if="isOwner" class="space-y-3">
      <!-- 판매 상태 변경 버튼 -->
      <div class="dropdown dropdown-top w-full">
        <div tabindex="0" role="button" class="btn btn-primary btn-lg w-full">
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
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          판매상태 변경
        </div>
        <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow-lg bg-base-100 rounded-box w-full mb-2 border border-base-content/10">
          <li>
            <button
              @click="emit('statusChange', 'available')"
              class="flex items-center justify-between"
              :class="{ 'active': props.status === 'available' }"
            >
              <span class="flex items-center">
                <span class="badge badge-success badge-sm mr-2"></span>
                판매중
              </span>
              <svg
                v-if="props.status === 'available'"
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
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </button>
          </li>
          <li>
            <button
              @click="emit('statusChange', 'reserved')"
              class="flex items-center justify-between"
              :class="{ 'active': props.status === 'reserved' }"
            >
              <span class="flex items-center">
                <span class="badge badge-warning badge-sm mr-2"></span>
                예약중
              </span>
              <svg
                v-if="props.status === 'reserved'"
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
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </button>
          </li>
          <li>
            <button
              @click="emit('statusChange', 'sold')"
              class="flex items-center justify-between"
              :class="{ 'active': props.status === 'sold' }"
            >
              <span class="flex items-center">
                <span class="badge badge-ghost badge-sm mr-2"></span>
                판매완료
              </span>
              <svg
                v-if="props.status === 'sold'"
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
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </button>
          </li>
        </ul>
      </div>

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
const props = defineProps({
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
  status: {
    type: String,
    default: 'available',
  },
  isLoggedIn: {
    type: Boolean,
    default: false,
  },
})

// ==================== Emits ====================
const emit = defineEmits(['delete', 'statusChange'])
</script>
