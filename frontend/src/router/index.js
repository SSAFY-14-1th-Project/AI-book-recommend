import Layout from '@/layout/Layout.vue'
import { createRouter, createWebHistory } from 'vue-router'
// 로그인된 사용자만 상세 페이지 보게 해야지..
import { useLoginStore } from '@/stores/loginStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/LoginView.vue'),
        },
        {
          path: 'signup',
          name: 'signup',
          component: () => import('@/views/SignupView.vue'),
        },
        // 추가
        {
          path: 'trades',
          name: 'trade-list',
          component: () => import('@/views/TradeListView.vue'),
        },
        {
          path: 'trades/create',
          name: 'trade-create',
          component: () => import('@/views/TradeCreateView.vue'),
          meta: { requiresAuth: true }  // 로그인 필요
        },
        {
          path: 'trades/:id',
          name: 'trade-detail',
          component: () => import('@/views/TradeDetailView.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'trades/:id/edit',
          name: 'trade-edit',
          component: () => import('@/views/TradeEditView.vue'),
          meta: { requiresAuth: true }
        },
      ],
    },
  ],
})

// 네비게이션 가드
router.beforeEach((to, from, next) => {
  const loginStore = useLoginStore()
  
  if (to.meta.requiresAuth && !loginStore.token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
