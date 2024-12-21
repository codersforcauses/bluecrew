<script setup lang="ts">
import { RouterView } from 'vue-router'
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import NavBarWrapper from '@/components/NavBarWrapper.vue'
</script>

<template>
  <v-app>
    <NavBarWrapper />
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
  <BluecrewFooter />
</template>

<style scoped></style>
