<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
</script>

<template>
  <WaveBanner image-src="teambuilding-background.jpg" />
  <h2 class="text-center text-primaryBlue mb-4">Admin</h2>
  <div class="d-flex flex-column align-center mt-5 px-5">
    <div v-for="row in 4" :key="row" class="d-flex flex-row ga-1 row mb-1">
      <v-text-field
        v-for="col in 4"
        :key="col"
        hide-details
        variant="outlined"
        bg-color="primaryBrown"
      />
    </div>
  </div>
</template>

<style scoped>
.row {
  max-width: 400px;
}
</style>
