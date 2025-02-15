<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'
import NavBarMobile from '@/components/NavBarMobile.vue'
import NavBarDesktop from '@/components/NavBarDesktop.vue'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
import type { NavigationInfo } from '@/types/navigation'

const userStore = useUserStore()
const modalStore = useModalStore()
const { smAndUp } = useDisplay()
const router = useRouter()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userName = computed(() => userStore.userData?.userName || '')
const truncatedUserName = computed(() => {
  return userName.value.length > 10 ? `${userName.value.slice(0, 10)}...` : userName.value
})

const baseNavigationInfo: NavigationInfo[] = [
  { name: 'Home', routerName: 'landing', requireAuth: false },
  { name: 'Blingo', routerName: 'blingo', requireAuth: false },
  { name: 'Leaderboard', routerName: 'leaderboard', requireAuth: false },
  { name: 'Friends', routerName: 'friends', requireAuth: true },
  { name: 'Preferences', routerName: 'preferences', requireAuth: true },
]

const pages = computed<NavigationInfo[]>(() => {
  if (userStore.superUserLoggedIn) {
    return [...baseNavigationInfo, { name: 'Admin', routerName: 'admin', requireAuth: true }]
  }
  return baseNavigationInfo
})

const handleAuth = async () => {
  if (isLoggedIn.value) {
    await userStore.logout()
  } else {
    modalStore.openLogin()
  }
}

const handleNavigation = (page: string) => {
  router.push({ name: page })
}

const handleSignInClick = (action: 'login' | 'register') => {
  if (action === 'login') {
    modalStore.openLogin()
  } else if (action === 'register') {
    modalStore.openRegister()
  }
}
</script>

<template>
  <div class="sticky-nav bg-primaryWhite">
    <!-- Desktop NavBar -->
    <div v-if="smAndUp" class="nav-bar-desktop">
      <NavBarDesktop
        :is-logged-in="isLoggedIn"
        :user-name="truncatedUserName"
        :pages="pages"
        @navigate="handleNavigation"
        @auth="handleAuth"
        @sign-in-click="handleSignInClick"
      />
    </div>

    <!-- Mobile NavBar -->
    <div v-else class="nav-bar-mobile">
      <NavBarMobile
        :is-logged-in="isLoggedIn"
        :user-name="truncatedUserName"
        :pages="pages"
        @navigate="handleNavigation"
        @auth="handleAuth"
        @sign-in-click="handleSignInClick"
      />
    </div>
  </div>
</template>

<style>
.sticky-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  box-shadow: none !important;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
