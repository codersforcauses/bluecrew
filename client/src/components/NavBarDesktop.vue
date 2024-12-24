<template>
  <v-toolbar class="nav-bar" density="comfortable">
    <v-spacer></v-spacer>
    <v-toolbar-items class="nav-bar-items">
      <v-btn @click="emit('navigate', 'home')">Home</v-btn>
      <v-btn @click="emit('navigate', 'leaderboard')">Leaderboard</v-btn>
      <v-btn
        :style="{ opacity: isLoggedIn ? 1 : 0.5 }"
        @click="emit('navigate', 'friends')"
      >
        Friends
      </v-btn>
      <v-btn
        :style="{ opacity: isLoggedIn ? 1 : 0.5 }"
        @click="emit('navigate', 'preferences')"
      >
        Preferences
      </v-btn>
      <v-btn @click="emit('auth')">{{ isLoggedIn ? 'Log Out' : 'Sign In' }}</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

defineProps({
  isLoggedIn: Boolean,
  userName: String,
});

const emit = defineEmits(['navigate', 'auth']);
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
  height: 48px;
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
