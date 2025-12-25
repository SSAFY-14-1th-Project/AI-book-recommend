<template>
  <div class="hero bg-base-200 min-h-screen px-5">
    <div class="hero-content flex-col lg:flex-row-reverse">
      <div class="text-center lg:text-left">
        <h2 class="text-5xl font-bold">동네 책방</h2>
        <div class="py-6 w-full min-w-max">
          <p>우리 동네에서 만나는 특별한 책 이야기.</p>
          <p>AI 추천부터 중고 거래까지, 당신의 책장을 채워보세요!</p>
        </div>
      </div>
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <form @submit.prevent="handleLogin" class="card-body">
          <h1 class="text-2xl font-bold flex justify-center">로그인</h1>
          <fieldset class="fieldset mt-5">
            <label for="username" class="label">아이디</label>
            <input
              type="text"
              id="username"
              name="username"
              autocomplete="username"
              class="input"
              placeholder="아이디를 입력해주세요"
              v-model="username"
            />
            <label for="password" class="label">비밀번호</label>
            <input
              type="password"
              id="password"
              name="password"
              autocomplete="current-password"
              class="input"
              placeholder="비밀번호를 입력해주세요"
              v-model="password"
            />
            <div class="flex gap-2">
              <RouterLink :to="{ name: 'signup' }" class="link link-hover">회원가입</RouterLink> |
              <RouterLink :to="{ name: 'home' }" class="link link-hover"
                >비회원으로 시작하기</RouterLink
              >
            </div>
            <button class="btn btn-neutral mt-4">로그인</button>
          </fieldset>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginStore } from '@/stores/loginStore'
import { getUser, login } from '@/api/accounts'

const router = useRouter()
const loginStore = useLoginStore()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  // 에러 메시지 초기화
  errorMessage.value = ''
  isLoading.value = true

  try {
    // 1. API 호출
    const tokens = await login({
      username: username.value,
      password: password.value,
    })

    // 2. Store에 토큰 저장
    loginStore.setTokens(tokens.access, tokens.refresh)

    // 3. user 정보 조회
    const user = await getUser()

    // 4. Store에 user 정보 저장
    loginStore.setUser(user)

    // 5. 홈 페이지로 이동
    router.push('/')
  } catch (error) {
    // 에러 처리
    console.error('로그인 실패:', error)
    errorMessage.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
  } finally {
    isLoading.value = false
  }
}
</script>
