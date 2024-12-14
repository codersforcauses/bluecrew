<template>
  <v-toolbar class="nav-bar" density="comfortable">
    <v-spacer></v-spacer>
    <v-toolbar-items class="nav-bar-items">
      <!-- Button of Home, Leaderboard, Friends & Preferences -->
      <v-btn :class="{ 'active-link': isActive('home') }" :to="{ name: 'home' }">Home</v-btn>
      <v-btn :class="{ 'active-link': isActive('leaderboard') }" :to="{ name: 'leaderboard' }"
        >Leaderboard</v-btn
      >
      <v-btn
        :class="{ 'active-link': isActive('friends') }"
        :style="{ opacity: isLoggedIn ? 1 : 0.5 }"
        @click="handleNavigation('friends')"
        >Friends</v-btn
      >
      <v-btn
        :class="{ 'active-link': isActive('preferences') }"
        :style="{ opacity: isLoggedIn ? 1 : 0.5 }"
        @click="handleNavigation('preferences')"
        >Preferences</v-btn
      >

      <!-- Logout Status -->
      <v-menu v-if="!isLoggedIn" open-on-hover offset-y>
        <template #activator="{ props }">
          <v-btn class="status-btn" v-bind="props">Sign In / Up</v-btn>
        </template>
        <v-list class="menu-list">
          <v-list-item class="menu-item" @click="modalStore.openLogin()">
            <v-list-item-title>Login</v-list-item-title>
          </v-list-item>
          <v-list-item class="menu-item" @click="modalStore.openRegister()">
            <v-list-item-title>Register</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <!-- Login Status -->
      <v-menu v-else open-on-hover offset-y>
        <template #activator="{ props }">
          <v-btn class="status-btn" v-bind="props">{{ truncatedUserName }}</v-btn>
        </template>
        <v-list class="menu-list">
          <v-list-item class="menu-item" @click="userStore.logout()">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'

const route = useRoute()
const router = useRouter()

const userStore = useUserStore()
const modalStore = useModalStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userName = computed(() => userStore.userData?.userName || '')

const isActive = (name: string) => {
  return route.name === name
}

//Navigate Logics to each pages
const handleNavigation = (page: string) => {
  if (!isLoggedIn.value) {
    alert('You must be logged in to access this page.')
    return
  }
  router.push({ name: page })
}

//truncate username if exceeds 10 characters
const truncatedUserName = computed(() => {
  if (isLoggedIn.value && userName.value.length > 10) {
    return userName.value.slice(0, 10) + '...'
  }
  return userName.value
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');

.nav-bar {
  display: flex;
  background-color: white;
  justify-content: center;
  align-items: center;
  position: fixed;
  width: auto;
  height: 104px;
  top: 52px;
  right: 55px;
  max-width: 100%;
  margin: 0 auto;
  z-index: 1000;
}

.nav-bar-items {
  display: flex;
  gap: 15px;
  justify-content: center;
  font-size: 20px;
  color: #d12974;
  text-transform: none;
  font-family: 'Lilita One', cursive;
}

.nav-bar-items .v-btn {
  text-transform: none !important;
  font-size: 20px;
  letter-spacing: -0.1px;
  font-weight: 500;
  color: #d12974;
  background-color: transparent;
}

.nav-bar-items .v-btn.active-link {
  color: #193855;
}

.menu-list .menu-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  font-family: 'Lilita One', cursive;
  font-size: 24px !important;
  font-weight: 600 !important;
  color: #d12974 !important;
  background-color: transparent !important;
  border-radius: 12px;
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}
</style>
