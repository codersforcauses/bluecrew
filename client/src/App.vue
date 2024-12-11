<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBarWrapper from '@/components/NavBarWrapper.vue';

</script>

<template>
  <v-app>
    <NavBarWrapper />
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
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