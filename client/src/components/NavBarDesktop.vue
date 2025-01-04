<template>
  <v-toolbar class="nav-bar" density="comfortable">
    <v-spacer></v-spacer>
    <v-toolbar-items class="nav-bar-items">
      <v-btn @click="$emit('navigate', 'home')">Home</v-btn>
      <v-btn @click="$emit('navigate', 'leaderboard')">Leaderboard</v-btn>
      <v-btn :style="{ opacity: isLoggedIn ? 1 : 0.5 }" @click="$emit('navigate', 'friends')">
        Friends
      </v-btn>
      <v-btn :style="{ opacity: isLoggedIn ? 1 : 0.5 }" @click="$emit('navigate', 'preferences')">
        Preferences
      </v-btn>
      <v-menu open-on-hover>
        <template #activator="{ props }">
          <v-btn v-bind="props" class="menu-list">
            {{ isLoggedIn ? 'Log Out' : 'Sign In' }}
          </v-btn>
        </template>
        <v-list v-if="!isLoggedIn" class="menu-item">
          <v-list-item class="menu-button" @click="$emit('sign-in-click', 'login')"
            >Log In</v-list-item
          >
          <v-list-item class="menu-button" @click="$emit('sign-in-click', 'register')"
            >Register</v-list-item
          >
        </v-list>
        <v-list v-else>
          <v-list-item @click="$emit('auth')">Log Out</v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

defineProps({
  isLoggedIn: Boolean,
  userName: String,
})

defineEmits(['navigate', 'auth', 'sign-in-click'])
</script>

<style scoped>
.nav-bar {
  display: flex;
  background-color: white;
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
  text-transform: none;
  font-size: 20px;
  letter-spacing: -0.1px;
  font-weight: 500;
  color: #d12974;
  background-color: transparent;
}

.nav-bar-items .v-btn.active-link {
  color: #193855;
}

.menu-item {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  height: 56px;
  font-family: 'Lilita One', cursive;
  font-size: 20px !important;
  font-weight: 500 !important;
  color: #d12974 !important;
  background-color: transparent !important;
  border-radius: 12px;
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

.menu-list .menu-item {
  width: 100%;
}
</style>
