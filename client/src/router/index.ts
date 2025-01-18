import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'

import PlaceholderView from '../views/PlaceHolderview.vue'
import LandingView from '@/views/LandingView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'
import FriendView from '@/views/FriendView.vue'
import BlingoView from '@/views/BlingoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/friends',
      name: 'friends',
      component: FriendView,
      meta: { requiresAuth: true },
    },
    {
      path: '/preferences',
      name: 'preferences',
      component: PlaceholderView,
      meta: { requiresAuth: true },
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView,
    },
    {
      path: '/blingo',
      name: 'blingo',
      component: BlingoView,
    },
    {
      path: '/404',
      name: '404',
      component: () => import('@/views/404Error.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404',
    },
    {
      path: '/404',
      name: '404',
      component: () => import('@/views/404Error.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404',
    },
  ],
})

router.beforeEach((to, from) => {
  const userStore = useUserStore()
  const modalStore = useModalStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    modalStore.openLogin()
    return { name: from.name }
  }

  return true
})

export default router
