import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FriendView from '../views/FriendView.vue'
import PreferencesView from '../views/PreferencesView.vue'
import { useModalStore } from '@/stores/modal'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
      component: PreferencesView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from) => {
  const modalStore = useModalStore()

  if (modalStore.currentModal === 'none') {
    modalStore.openRegister()
    return false
  }

  return true
})

export default router
