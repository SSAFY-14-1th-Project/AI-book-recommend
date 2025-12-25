<template>
  <div class="hero bg-base-200 min-h-screen px-5">
    <div class="hero-content flex-col lg:flex-row-reverse w-full">
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl py-5">
        <div class="flex flex-col items-center gap-3">
          <h1 class="text-2xl font-bold">회원가입</h1>
          <p>새 계정을 만들어주세요!</p>
        </div>

        <form @submit.prevent="handleSignup" class="card-body">
          <fieldset class="fieldset">
            <!-- 아이디 -->
            <label for="username" class="label">아이디 <span class="text-red-500">*</span></label>
            <input
              type="text"
              id="username"
              name="username"
              autocomplete="username"
              class="input"
              placeholder="아이디"
              v-model="username"
            />
            <!-- 비밀번호 -->
            <label class="label" for="password">비밀번호 <span class="text-red-500">*</span></label>
            <input
              type="password"
              id="password"
              name="password"
              autocomplete="new-password"
              class="input"
              placeholder="비밀번호"
              v-model="password"
            />
            <!-- 비밀번호 확인 -->
            <label for="passwordConfirm" class="label"
              >비밀번호 확인 <span class="text-red-500">*</span></label
            >
            <input
              type="password"
              id="passwordConfirm"
              name="passwordConfirm"
              autocomplete="new-password"
              class="input"
              placeholder="비밀번호 확인"
              v-model="passwordConfirm"
            />
            <!-- 이메일 -->
            <label for="email" class="label">이메일</label>
            <input
              type="email"
              id="email"
              name="email"
              autocomplete="email"
              class="input"
              placeholder="example@email.com"
              v-model="email"
            />
            <!-- 에러 메시지 -->
            <div v-if="errorMessage" class="text-sm text-red-600">
              {{ errorMessage }}
            </div>
            <!-- 회원가입 버튼 -->
            <button class="btn btn-neutral mt-4">회원가입</button>
            <!-- 로그인 링크 -->
            <div class="flex gap-2">
              <span>이미 계정이 있으신가요?</span>
              <RouterLink :to="{ name: 'login' }" class="link link-hover text-secondary-content"
                >로그인</RouterLink
              >
            </div>
          </fieldset>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { signup } from '@/api/accounts'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const passwordConfirm = ref('')
const email = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleSignup = async () => {
  // 초기화
  errorMessage.value = ''
  successMessage.value = ''

  // 비밀번호 일치 확인
  if (password.value !== passwordConfirm.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  // 비밀번호 길이 확인
  if (password.value.length < 8) {
    errorMessage.value = '비밀번호는 8자 이상이어야 합니다.'
    return
  }

  isLoading.value = true

  try {
    // 회원가입 API 호출
    await signup({
      username: username.value,
      email: email.value,
      password: password.value,
      passwordConfirm: passwordConfirm.value, // camelCase (자동 변환됨)
    })

    // 성공 메시지
    successMessage.value = '회원가입이 완료되었습니다!'
    // TODO : 성공 메시지 토스트 띄우기
    alert(successMessage.value)

    router.push('/login')
  } catch (error) {
    console.error('회원가입 실패:', error)

    // 서버에서 온 에러 메시지 처리
    if (error.response?.data) {
      const errorData = error.response.data

      // Django REST Framework 에러 형식 (camelCase로 자동 변환됨)
      if (errorData.username) {
        errorMessage.value = `아이디: ${errorData.username[0]}`
      } else if (errorData.email) {
        errorMessage.value = `이메일: ${errorData.email[0]}`
      } else if (errorData.password) {
        errorMessage.value = `비밀번호: ${errorData.password[0]}`
      } else if (errorData.passwordConfirm) {
        errorMessage.value = `비밀번호 확인: ${errorData.passwordConfirm[0]}`
      } else if (errorData.nonFieldErrors) {
        errorMessage.value = errorData.nonFieldErrors[0]
      } else {
        // 전체 에러 메시지 표시 (디버깅용)
        const errorMessages = Object.entries(errorData)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value[0] : value}`)
          .join(', ')
        errorMessage.value = errorMessages || '회원가입에 실패했습니다. 다시 시도해주세요.'
      }
    } else {
      errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
