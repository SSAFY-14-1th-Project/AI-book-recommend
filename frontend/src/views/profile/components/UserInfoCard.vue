<template>
  <!-- ==================== 사용자 정보 카드 ==================== -->
  <div class="card bg-base-100 shadow-lg border border-base-content/10">
    <div class="card-body p-8">
      <div class="flex items-start justify-between mb-6">
        <h2 class="text-2xl font-bold">내 프로필</h2>
        <button @click="$emit('edit')" class="btn btn-primary btn-sm">
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
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
          정보 수정
        </button>
      </div>

      <div class="space-y-6">
        <!-- 닉네임 -->
        <div class="flex items-center gap-4">
          <div>
            <div class="text-sm text-base-content/60">닉네임</div>
            <div class="text-xl font-bold">{{ user?.nickname || '미설정' }}</div>
          </div>
        </div>

        <!-- 구분선 -->
        <div class="divider my-4"></div>

        <!-- 기본 정보 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- 아이디 -->
          <div class="space-y-1">
            <div class="text-sm text-base-content/60">아이디</div>
            <div class="font-medium">{{ user?.username }}</div>
          </div>

          <!-- 나이 -->
          <div class="space-y-1">
            <div class="text-sm text-base-content/60">나이</div>
            <div class="font-medium">{{ user?.age || '미설정' }}세</div>
          </div>

          <!-- 이메일 -->
          <div class="space-y-1">
            <div class="text-sm text-base-content/60">이메일</div>
            <div class="font-medium">{{ user?.email || '미설정' }}</div>
          </div>
        </div>

        <!-- 구분선 -->
        <div class="divider my-4"></div>

        <!-- 독서 MBTI -->
        <div v-if="user?.bookMbti" class="space-y-3">
          <div class="text-sm text-base-content/60">독서 MBTI</div>
          <div
            class="bg-linear-to-br from-primary/10 to-secondary/10 rounded-lg p-4 border border-primary/20"
          >
            <div class="flex items-center gap-4">
              <div class="text-3xl font-bold text-primary">
                {{ user.bookMbti }}
              </div>
              <div class="flex-1">
                <div class="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span class="font-semibold">{{ user.bookMbti[0] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ user.bookMbti[0] === 'F' ? '지식형' : '이야기형' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ user.bookMbti[1] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ user.bookMbti[1] === 'R' ? '현실형' : '상상형' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ user.bookMbti[2] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ user.bookMbti[2] === 'E' ? '가벼운' : '깊은' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ user.bookMbti[3] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ user.bookMbti[3] === 'P' ? '빠른전개' : '느린전개' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="alert alert-warning">
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
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <span>독서 MBTI가 설정되지 않았습니다. 정보 수정에서 설정해주세요.</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// ==================== Props & Emits ====================
const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})

defineEmits(['edit'])
</script>
