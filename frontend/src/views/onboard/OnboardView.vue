<template>
  <main class="bg-gradient-to-br from-primary/5 via-base-100 to-secondary/5 min-h-screen">
    <div class="container mx-auto px-4 py-12 max-w-4xl">
      <!-- 헤더 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold mb-4">
          {{ isEditing ? '프로필 수정' : '환영합니다!' }}
        </h1>
        <p class="text-lg text-base-content/70">
          {{ isEditing ? '정보를 수정해주세요' : '당신의 독서 취향을 알려주세요' }}
        </p>
      </div>

      <!-- 진행 상태 표시 -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medium">진행률</span>
          <span class="text-sm font-medium">{{ currentStep }}/5</span>
        </div>
        <progress
          class="progress progress-primary w-full"
          :value="currentStep"
          max="5"
        ></progress>
      </div>

      <!-- Step 1-4: MBTI 질문 -->
      <div v-if="currentStep <= 4" class="space-y-6">
        <MBTIQuestion
          :question-number="currentStep"
          :type-label="mbtiQuestions[currentStep - 1].typeLabel"
          :question="mbtiQuestions[currentStep - 1].question"
          :options="mbtiQuestions[currentStep - 1].options"
          :selected="mbtiAnswers[currentStep - 1]"
          @select="handleMBTISelect"
        />

        <!-- 네비게이션 버튼 -->
        <div class="flex gap-3">
          <button
            v-if="currentStep > 1"
            type="button"
            @click="currentStep--"
            class="btn btn-outline"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            이전
          </button>
          <button
            type="button"
            @click="nextStep"
            :disabled="!mbtiAnswers[currentStep - 1]"
            class="btn btn-primary flex-1"
          >
            다음
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
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Step 5: 기본 정보 입력 -->
      <div v-else class="space-y-6">
        <BasicInfoForm
          v-model:nickname="form.nickname"
          v-model:age="form.age"
        />

        <!-- 결과 MBTI 표시 -->
        <div class="card bg-gradient-to-br from-primary/10 to-secondary/10 shadow-lg border border-primary/20">
          <div class="card-body p-6">
            <h3 class="text-lg font-bold mb-3">당신의 독서 MBTI</h3>
            <div class="flex items-center gap-4">
              <div class="text-4xl font-bold text-primary">
                {{ calculatedMBTI }}
              </div>
              <div class="flex-1">
                <div class="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span class="font-semibold">{{ mbtiAnswers[0] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ mbtiAnswers[0] === 'F' ? '지식형' : '이야기형' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ mbtiAnswers[1] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ mbtiAnswers[1] === 'R' ? '현실형' : '상상형' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ mbtiAnswers[2] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ mbtiAnswers[2] === 'E' ? '가벼운' : '깊은' }}
                    </span>
                  </div>
                  <div>
                    <span class="font-semibold">{{ mbtiAnswers[3] }}</span>
                    <span class="text-base-content/60 ml-1">
                      {{ mbtiAnswers[3] === 'P' ? '빠른전개' : '느린전개' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 제출 버튼 -->
        <div class="flex gap-3">
          <button
            type="button"
            @click="currentStep--"
            class="btn btn-outline"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            이전
          </button>
          <button
            type="button"
            @click="handleSubmit"
            :disabled="!form.nickname || !form.age || isSubmitting"
            class="btn btn-primary flex-1"
          >
            <svg
              v-if="!isSubmitting"
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
            <span v-if="isSubmitting" class="loading loading-spinner"></span>
            {{ isEditing ? '수정 완료' : '시작하기' }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLoginStore } from '@/stores/loginStore'
import { updateProfile } from '@/api/accounts'
import MBTIQuestion from './components/MBTIQuestion.vue'
import BasicInfoForm from './components/BasicInfoForm.vue'

// ==================== 라우터 & 스토어 ====================
const router = useRouter()
const route = useRoute()
const loginStore = useLoginStore()

// ==================== 상태 관리 ====================
const currentStep = ref(1)
const isSubmitting = ref(false)

// MBTI 답변 (4개)
const mbtiAnswers = ref(['', '', '', ''])

// 기본 정보 폼
const form = ref({
  nickname: '',
  age: 0,
})

// 수정 모드 여부
const isEditing = computed(() => route.query.edit === 'true')

// ==================== MBTI 질문 데이터 ====================
const mbtiQuestions = [
  {
    typeLabel: 'Story vs Fact',
    question: '책을 고를 때 더 끌리는 쪽은 어느 쪽인가요?',
    options: [
      {
        value: 'F',
        label: 'Fact (지식형)',
        description: '지식·정보·현실 이야기를 배우는 책',
      },
      {
        value: 'S',
        label: 'Story (이야기형)',
        description: '이야기와 감정에 몰입할 수 있는 책',
      },
    ],
  },
  {
    typeLabel: 'Realistic vs Imaginary',
    question: '배경이 중요한 책이라면, 어떤 세계가 더 좋나요?',
    options: [
      {
        value: 'R',
        label: 'Realistic (현실형)',
        description: '실제 현실을 바탕으로 한 이야기',
      },
      {
        value: 'I',
        label: 'Imaginary (상상형)',
        description: '상상 속 세계관이나 판타지·SF',
      },
    ],
  },
  {
    typeLabel: 'Easy vs Deep',
    question: '읽는 난이도에 대해 더 선호하는 쪽은?',
    options: [
      {
        value: 'E',
        label: 'Easy (가벼운)',
        description: '가볍고 술술 읽히는 책',
      },
      {
        value: 'D',
        label: 'Deep (깊은)',
        description: '문장이 깊고 생각할 거리가 많은 책',
      },
    ],
  },
  {
    typeLabel: 'Pace vs Chunk',
    question: '전개 방식은 어떤 쪽이 더 좋나요?',
    options: [
      {
        value: 'P',
        label: 'Pace (빠른전개)',
        description: '전개가 빠르고 짧은 챕터 구성',
      },
      {
        value: 'C',
        label: 'Chunk (느린전개)',
        description: '분량이 많고 천천히 쌓아가는 이야기',
      },
    ],
  },
]

// ==================== Computed ====================
const calculatedMBTI = computed(() => {
  return mbtiAnswers.value.join('')
})

// ==================== Methods ====================
// MBTI 선택 처리
const handleMBTISelect = (value) => {
  mbtiAnswers.value[currentStep.value - 1] = value
}

// 다음 단계로
const nextStep = () => {
  if (currentStep.value < 5) {
    currentStep.value++
  }
}

// MBTI 코드를 ID로 변환
const getMBTIId = (mbtiCode) => {
  // F=0, S=1 / R=0, I=1 / E=0, D=1 / P=0, C=1
  // ID = 1 + (첫째*8 + 둘째*4 + 셋째*2 + 넷째*1)
  const mapping = {
    F: 0, S: 1,
    R: 0, I: 1,
    E: 0, D: 1,
    P: 0, C: 1,
  }

  const values = mbtiCode.split('').map(char => mapping[char])
  const id = 1 + (values[0] * 8 + values[1] * 4 + values[2] * 2 + values[3])
  return id
}

// 제출 처리
const handleSubmit = async () => {
  if (!form.value.nickname || !form.value.age) {
    alert('닉네임과 나이를 입력해주세요.')
    return
  }

  if (calculatedMBTI.value.length !== 4) {
    alert('모든 질문에 답변해주세요.')
    return
  }

  isSubmitting.value = true

  try {
    const mbtiCode = calculatedMBTI.value
    const mbtiId = getMBTIId(mbtiCode)

    // 프로필 업데이트
    const profileData = {
      nickname: form.value.nickname,
      age: form.value.age,
      book_mbti: mbtiId, // BookMBTI ID 전송
    }

    const updatedUser = await updateProfile(profileData)

    // 스토어 업데이트
    loginStore.setUser(updatedUser)

    alert(isEditing.value ? '프로필이 수정되었습니다!' : '환영합니다! 맞춤 도서 추천을 시작합니다.')
    router.push({ name: 'home' })
  } catch (error) {
    console.error('프로필 업데이트 실패:', error)

    if (error.response?.data) {
      const errors = error.response.data
      const message = Object.values(errors).flat().join('\n')
      alert(`오류가 발생했습니다\n\n${message}`)
    } else {
      alert('프로필 업데이트에 실패했습니다. 다시 시도해주세요.')
    }
  } finally {
    isSubmitting.value = false
  }
}

// ==================== Lifecycle ====================
onMounted(() => {
  // 수정 모드인 경우 기존 정보 로드
  if (isEditing.value && loginStore.user) {
    form.value.nickname = loginStore.user.nickname || ''
    form.value.age = loginStore.user.age || 0

    // 기존 MBTI가 있으면 로드
    if (loginStore.user.book_mbti) {
      const mbtiCode = loginStore.user.book_mbti
      mbtiAnswers.value = mbtiCode.split('')
    }
  }
})
</script>
