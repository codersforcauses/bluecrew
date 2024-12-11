<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBarMobile from '@/components/NavBarMobile.vue'
</script>

<template>
  <div>
    <NavBarMobile />
    <RouterView />
  </div>
</template>

<style>
/* Reset default margins and padding */
body {
  margin: 0;
  padding: 0;
}

/* Ensure full height for app container */
#app {
  min-height: 100vh;
}
</style>