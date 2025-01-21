<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useDisplay } from 'vuetify'
import { ref } from 'vue'

const { xs } = useDisplay()

// Sample data - replace with actual data source
const username = ref('Username')
const fullName = ref('Firstname Lastname')
const bio = ref('This is a bio.')
const totalPoints = ref('1000pts')
</script>

<template>
  <v-container fluid class="pa-0 d-flex flex-column">
    <!-- Wave Banner -->
    <v-row v-if="!xs" class="header">
      <WaveBanner imageSrc="/beach-header.jpg" />
      <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
    </v-row>

    <!-- Profile Content -->
    <v-row class="px-16">
      <v-col cols="12" class="d-flex flex-column">
        <!-- Avatar and Name Section -->
        <div class="d-flex align-start mb-4">
            <v-img
                class="rounded-circle"
                max-height="96"
                max-width="96"
                min-width="96"
                cover
                src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
                ></v-img>
        </div>
      </v-col>
    </v-row>
    <v-row class="px-16">
      <v-col cols="12" class="d-flex flex-column">
        <h2 class="text-h4 font-weight-bold mb-1">{{ username }}</h2>
        <h3 class="text-h6 mb-1">{{ fullName }}</h3>
        <p class="mb-1">{{ bio }}</p>
        <p class="text-body-1">Total Point: {{ totalPoints }}</p>
      </v-col>
    </v-row>
    <!-- Edit Profile Section -->
    <v-row class="px-16">
      <v-col cols="11">
        <h2 class="text-h6 font-weight-bold mb-2">Edit Profile (Avatar, Bio & Visibility)</h2>
      </v-col>
      <v-col>
        <v-btn
        class="bg-primaryBlue rounded-xl"
        prepend-icon="mdi-pencil"
      >
        Edit Profile
      </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.header {
  width: 100%;
  height: 200px;
  position: relative;
  overflow: hidden;
}

.header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h3 {
  color: rgb(var(--v-theme-lightBlue));
}
</style>