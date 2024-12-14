import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlaceholderView from '../views/PlaceHolderview.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // Placeholder Views
    { path: '/leaderboard', name: 'leaderboard', component: PlaceholderView },
    { path: '/friends', name: 'friends', component: PlaceholderView },
    { path: '/preferences', name: 'preferences', component: PlaceholderView },
  ],
})

export default router
