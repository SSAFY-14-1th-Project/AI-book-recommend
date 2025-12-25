import Layout from '@/layout/Layout.vue'
import { createRouter, createWebHistory } from 'vue-router'

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
        },
      ],
    },
  ],
})

export default router
