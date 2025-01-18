<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { useDisplay } from 'vuetify'
import { ref } from 'vue'

const { xs } = useDisplay()
</script>

<template>
    <v-container fluid class="fill-height pa-0 flex-column">
        <v-row v-if="!xs" class="header">
            <WaveBanner imageSrc="/beach-header.jpg" />
            <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
        </v-row>
        
        <v-row class="flex-grow-1 w-100" align="center">
            <v-col align-start>
                <v-img
                class="rounded-circle"
                max-height="96"
                max-width="96"
                min-width="96"
                cover
                src="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"
                ></v-img>
            </v-col>

            <v-col>
                <v-text class="me-auto font-weight-bold truncate-name">{{ username }}</v-text>
                <v-text class="me-auto font-weight-bold truncate-name">{{ name }}</v-text>
            </v-col>

            <v-spacer></v-spacer>

            <v-text></v-text>
            <v-text></v-text>

            <v-btn class="bg-primaryBlue" prepend-icon="mdi-edit">
                <template v-slot:prepend>
                    <v-icon color="rgb(var(--v-theme-primaryGrey))"></v-icon>
                </template>
                Edit Profile
            </v-btn>

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