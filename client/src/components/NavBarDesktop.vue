<template>
  <v-toolbar class="nav-bar" density="comfortable">
    <v-spacer></v-spacer>
    <v-toolbar-items class="nav-bar-items">
      <v-btn text :class="{'active-link': isActive('home')}" :to="{ name: 'home' }">Home</v-btn>
      <v-btn text :class="{'active-link': isActive('leaderboard')}" :to="{ name: 'leaderboard' }">Leaderboard</v-btn>
      <v-btn text :class="{'active-link': isActive('friends')} " :style="{opacity: isLoggedIn ? 1 : 0.5}" @click="handleNavigation('friends')">Friends</v-btn>
      <v-btn text :class="{'active-link': isActive('preferences')}" :style="{opacity: isLoggedIn ? 1 : 0.5}" @click="handleNavigation('preferences')">Preferences</v-btn>

      <v-btn text class="status-btn" v-if="isLoggedIn">{{ userName }}</v-btn>
      <v-btn text class="status-btn" v-else :to="{ name: 'login' }">Login</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const isLoggedIn = ref(false); 
const userName = ref('User123');


window.isLoggedIn = isLoggedIn;
window.userName = userName;

const isActive = (name: string) => {
  return route.name === name;
};

const handleNavigation = (page: string) => {
  if (!isLoggedIn.value) {
    alert('You must be logged in to access this page.');
    return; 
  }
  router.push({ name: page }); 
};

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
  color: #D12974;
  text-transform: none;
  font-family: 'Lilita One', cursive;
}

.nav-bar-items .v-btn {
  text-transform: none !important;
  font-size: 20px;
  letter-spacing: -0.1px;
  font-weight: 500;
  color: #D12974;
  background-color: transparent;
}

.nav-bar-items .v-btn.active-link {
  color: #193855;
}
</style>
