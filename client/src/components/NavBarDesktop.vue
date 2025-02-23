<template>
  <v-toolbar class="nav-bar bg-primaryWhite" density="comfortable">
    <v-spacer />
    <v-toolbar-items class="nav-bar-items">
      <v-btn
        v-for="(page, index) in pages"
        :key="index"
        :style="{ opacity: !page.requireAuth || isLoggedIn ? 1 : 0.5 }"
        class="text-primaryGreen"
        @click="$emit('navigate', page.routerName)"
      >
        {{ page.name }}
      </v-btn>
      <v-menu open-on-hover>
        <template #activator="{ props }">
          <v-btn v-bind="props" class="menu-list text-primaryGreen">
            {{ isLoggedIn ? 'Log Out' : 'Sign In' }}
          </v-btn>
        </template>
        <v-list v-if="!isLoggedIn" class="menu-item">
          <v-list-item
            class="menu-button text-primaryGreen bg-primaryWhite"
            @click="$emit('sign-in-click', 'login')"
            >Log In</v-list-item
          >
          <v-list-item
            class="menu-button text-primaryGreen bg-primaryWhite"
            @click="$emit('sign-in-click', 'register')"
            >Register</v-list-item
          >
        </v-list>
        <v-list v-else class="menu-item">
          <v-list-item class="menu-button text-primaryGreen bg-primaryWhite" @click="$emit('auth')"
            >Log Out</v-list-item
          >
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script setup lang="ts">
import type { NavigationInfo } from '@/types/navigation'

defineProps<{
  isLoggedIn: boolean
  userName: string
  pages: NavigationInfo[]
}>()

defineEmits(['navigate', 'auth', 'sign-in-click'])
</script>

<style scoped>
.nav-bar {
  display: flex;
}

.nav-bar-items {
  display: flex;
  gap: 15px;
  justify-content: center;
  font-size: 20px;
  text-transform: none;
  font-family: 'Lilita One', cursive;
}

.nav-bar-items .v-btn {
  text-transform: none;
  font-size: 20px;
  letter-spacing: -0.1px;
  font-weight: 500;
  background-color: transparent;
}

.menu-item {
  display: flex;
  width: 100%;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  height: 56px;
  font-family: 'Lilita One', cursive;
  font-size: 20px !important;
  font-weight: 500 !important;
  border-radius: 12px;
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

.menu-list .menu-item {
  width: 100%;
}
</style>
