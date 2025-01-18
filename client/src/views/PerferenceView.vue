<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()
</script>

<template>
    <v-container fluid class="fill-height pa-0 flex-column">
        <v-row v-if="!xs" class="header">
            <WaveBanner imageSrc="/beach-header.jpg" />
            <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
        </v-row>
        
        <v-row class="flex-grow-1 w-100" align="center">
        </v-row>
    </v-container>
</template>

<style scoped>
.header {
  width: 100%;
  height: 200px;
  position: relative;
  overflow: hidden;
  flex-grow: 0;
  flex-shrink: 1;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: boxed;
}
</style>