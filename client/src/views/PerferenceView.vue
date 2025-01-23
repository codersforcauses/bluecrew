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
const isEditing = ref(false)
const selectedAvatar = ref(0)
const visibility = ref('Bluecrew only')

// Avatar options
const avatarOptions = [
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
  { src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg' },
]

const handleEditClick = () => {
  isEditing.value = true
}

const handleCancel = () => {
  isEditing.value = false
}

const handleApply = () => {
  // Add stuff here 
  isEditing.value = false
}
</script>

<template>
  <v-container fluid class="pa-0 d-flex flex-column">
    <!-- Wave Banner in Both States -->
    <v-row v-if="!xs" class="header">
      <WaveBanner imageSrc="/beach-header.jpg" />
      <img src="/beach-header.jpg" alt="Ocean Beach" class="header-image" />
    </v-row>

    <!-- Main Profile View -->
    <template v-if="!isEditing">
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
          <h3 class="text-h6 font-weight-bold mb-2">Edit Profile (Avatar, Bio & Visibility)</h3>
        </v-col>
        <v-col>
          <v-btn
            class="bg-primaryBlue rounded-xl"
            prepend-icon="mdi-pencil"
            @click="handleEditClick"
          >
            Edit Profile
          </v-btn>
        </v-col>
      </v-row>
    </template>

    <!-- Edit Profile View -->
    <template v-else>
      <v-container class="pa-4">
        <v-row>
          <v-col cols="9">
            <!-- Avatar Selection -->
            <v-row>
              <v-col cols="12">
                <h3 class="mb-4">Avatar</h3>
                <div class="d-flex flex-wrap gap-4">
                  <v-img
                    v-for="(avatar, index) in avatarOptions"
                    :key="index"
                    :src="avatar.src"
                    max-height="96"
                    max-width="96"
                    min-width="96"
                    cover
                    class="rounded-circle cursor-pointer"
                    :class="{ 'border-primary': selectedAvatar === index }"
                    @click="selectedAvatar = index"
                  />
                </div>
              </v-col>
            </v-row>

            <!-- Bio Section -->
            <v-row>
              <v-col cols="12">
                <h3 class="mb-4">Bio</h3>
                <v-textarea
                  v-model="bio"
                  variant="outlined"
                  bg-color="rgb(var(--v-theme-primaryBrown))"
                ></v-textarea>
              </v-col>
            </v-row>

            <!-- Visibility Section -->
            <v-row>
              <v-col cols="12">
                <h3 class="mb-4">Visibility</h3>
                <v-btn-toggle v-model="visibility">
                  <v-btn value="Bluecrew only">Bluecrew only</v-btn>
                  <v-btn value="Friend only">Friend only</v-btn>
                  <v-btn value="bals">Public</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
          </v-col>
            <!-- Action Buttons -->
          <v-col cols="3">
            <v-row>
              <v-col cols="12">
                <v-btn 
                  prepend-icon="mdi-content-save"
                  color="primaryBlue"
                  @click="handleApply"
                >
                  Apply
                </v-btn>
              </v-col>
              <v-col cols="12">
                <v-btn
                  prepend-icon="mdi-close"
                  variant="outlined"
                  @click="handleCancel"
                >
                  Cancel
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </template>
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
  color: rgb(var(--v-theme-primaryGreen));
}

.cursor-pointer {
  cursor: pointer;
}

.border-primary {
  border: 2px solid rgb(var(--v-theme-primary));
}

.gap-4 {
  gap: 1rem;
}

.v-btn-toggle {
  flex-direction: column;
}

:deep(.v-btn-group) {
  flex-direction: column;
}
</style>