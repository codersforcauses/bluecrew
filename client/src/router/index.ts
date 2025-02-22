import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
import type { RouteLocationNormalized } from 'vue-router'

import LandingView from '@/views/LandingView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'
import FriendView from '@/views/FriendView.vue'
import BlingoView from '@/views/BlingoView.vue'
import PreferenceView from '@/views/PreferenceView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ForgotPasswordView from '@/views/ForgotPasswordView.vue'
import EmailVerificationView from '@/views/EmailVerificationView.vue'
import AdminView from '@/views/AdminView.vue'

export const navigateToProfile = (username: string) => {
  router.push({
    name: 'user-profile', // name of the route we want to navigate to
    query: { username },
  })
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/profile',
      name: 'user-profile',
      component: ProfileView,
      props: (route: RouteLocationNormalized) => ({
        username: route.query.username as string | undefined,
      }),
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
      component: PreferenceView,
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
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, requiresAdmin: true },
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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: ForgotPasswordView,
      props: (route) => ({ token: route.query.token, uid: route.query.uid64 }),
    },
    {
      path: '/verify-email',
      name: 'verifyEmail',
      component: EmailVerificationView,
      props: (route) => ({ token: route.query.token, uid: route.query.uid64 }),
    },
  ],
})

router.beforeEach((to, from) => {
  const userStore = useUserStore()
  const modalStore = useModalStore()

  if (
    (to.meta.requiresAuth && !userStore.isLoggedIn) ||
    (to.meta.requiresAdmin && !userStore.superUserLoggedIn)
  ) {
    modalStore.openLogin()
    return { name: from.name }
  }

  return true
})

export default router
