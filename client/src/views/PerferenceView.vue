<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { ref } from 'vue'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()

// to be edited with stuff from user store
const username = ref('Username')
const fullName = ref('Firstname Lastname')
const bio = ref('This is a bio.')
const totalPoints = ref('1000pts')
const isEditing = ref(false)
const selectedAvatar = ref(0)
const visibility = ref('Bluecrew only')

const avatarOptions = [
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
  {
    src: 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg',
  },
]

const handleEditClick = () => {
  isEditing.value = true
}

const handleCancel = () => {
  isEditing.value = false
}

const handleApply = () => {
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
      <v-row class="px-4 px-sm-16">
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

      <v-row class="px-4 px-sm-16">
        <v-col cols="12" class="d-flex flex-column">
          <p class="text-h4 font-weight-bold mb-1">{{ username }}</p>
          <h3 class="text-h6 mb-1">{{ fullName }}</h3>
          <p class="mb-1">{{ bio }}</p>
          <p class="text-body-1">Total Point: {{ totalPoints }}</p>
        </v-col>
      </v-row>

      <!-- Edit Profile Section -->
      <v-row class="px-4 px-sm-16" no-gutters>
        <v-col cols="12">
          <p class="text-h6 font-weight-bold mb-2">Edit Profile (Avatar, Bio & Visibility)</p>
        </v-col>
        <v-col cols="12 mb-4">
          <v-btn
            class="bg-primaryBlue"
            prepend-icon="mdi-pencil"
            :block="xs"
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
          <v-col :cols="xs ? 12 : 9">
            <!-- Avatar Selection -->
            <v-row>
              <v-col cols="12">
                <p class="text-h6 font-weight-bold mb-4">Avatar</p>
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
                <p class="text-h6 font-weight-bold mb-4">Bio</p>
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
                <p class="text-h6 font-weight-bold mb-4">Visibility</p>
                <v-item-group
                  mandatory
                  class="d-flex flex-column"
                  selected-class="bg-primaryGreen"
                  v-model="visibility"
                >
                  <v-btn class="mb-2 bg-primaryBrown" variant="outlined" value="Bluecrew only"
                    >Bluecrew only</v-btn
                  >
                  <v-btn class="mb-2 bg-primaryBrown" variant="outlined" value="Friend only"
                    >Friend only</v-btn
                  >
                  <v-btn class="bg-primaryBrown" variant="outlined" value="Public">Public</v-btn>
                </v-item-group>
              </v-col>
            </v-row>
          </v-col>
          <!-- Action Buttons -->
          <v-col :cols="xs ? 12 : 3">
            <v-row>
              <v-col cols="12">
                <v-btn
                  class="d-flex"
                  prepend-icon="mdi-content-save"
                  color="primaryBlue"
                  block
                  @click="handleApply"
                >
                  Apply
                </v-btn>
              </v-col>
              <v-col cols="12">
                <v-btn
                  class="d-flex"
                  prepend-icon="mdi-close"
                  variant="outlined"
                  block
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
  border: 3px solid rgb(var(--v-theme-primaryGreen));
}

.gap-4 {
  gap: 48px;
}
</style>
