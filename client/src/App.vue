<script setup lang="ts">
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import NavBarWrapper from '@/components/NavBarWrapper.vue'
</script>

<template>
  <v-app>
    <!-- Navigation Bar -->
    <NavBarWrapper />

    <!-- Main Content -->
    <v-main class="main-content">
      <RouterView />
    </v-main>

    <!-- Footer -->
    <BluecrewFooter />
  </v-app>
</template>

<style scoped>
.main-content {
  margin-top: 56px;
}
</style>
