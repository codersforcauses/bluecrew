<script setup lang="ts">
import BluecrewFooter from '@/components/BluecrewFooter.vue'
import NavBarWrapper from '@/components/NavBarWrapper.vue'
</script>

<template>
  <v-theme-provider theme="colourTheme">
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
  </v-theme-provider>
</template>

<style scoped>
.main-content {
  margin-top: 56px;
}
</style>
