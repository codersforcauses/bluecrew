<script setup lang="ts">
import WaveBanner from '@/components/WaveBanner.vue'
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
import avatarPaths from '@/utils/avatar'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types/user'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'
import type { ExtendedAxiosError } from '@/types/other'

const { xs } = useDisplay()
const userStore = useUserStore()

const bio = ref<string>('')
const isEditing = ref(false)
const visOptions = ['Bluecrew only', 'Friends only', 'Public']
const visibility = ref<0 | 1 | 2>(0)
const bioError = ref<string>('')
const messageStore = useMessageStore()
const selectedAvatar = ref<0 | 1 | 2 | 3 | 4 | 5>(0)
const loading = ref(false)

const handleEditClick = () => {
  isEditing.value = true
  const nonNullUser = userStore.userData as User
  bio.value = nonNullUser.bio
  visibility.value = nonNullUser.visibility
  selectedAvatar.value = nonNullUser.avatar
}

const handleCancel = () => {
  isEditing.value = false
}

const handleApply = () => {
  loading.value = true

  server
    .put('update-preferences/', {
      avatar: selectedAvatar.value,
      bio: bio.value,
      visibility: visibility.value,
    })
    .then(() => {
      const nonNullUser = userStore.userData!
      nonNullUser.avatar = selectedAvatar.value
      nonNullUser.bio = bio.value
      nonNullUser.visibility = visibility.value
      isEditing.value = false
      messageStore.showMessage('Success', 'Preferences successfully changed!', 'success')
    })
    .catch((error: ExtendedAxiosError) => {
      if (
        error.response &&
        error.response.status === 400 &&
        'bio' in (error.response.data as object)
      ) {
        bioError.value = 'Please enter a bio with at most 300 characters'
      } else {
        messageStore.handleUnexpectedError(error.config?.session_expired, false)
      }
    })
    .finally(() => {
      loading.value = false
    })
}
</script>

<template>
  <WaveBanner imageSrc="/drone-beach.jpg" altText="Drone shot of a beach" />
  <v-container fluid class="pa-0 d-flex flex-column" v-if="userStore.userData">
    <!-- Main Profile View -->
    <template v-if="!isEditing">
      <!-- Profile Content -->
      <v-row class="px-4 px-sm-16 mx-0 pt-4">
        <v-col cols="12" class="d-flex flex-column">
          <!-- Avatar and Name Section -->
          <div class="d-flex align-start mb-4">
            <v-img
              class="rounded-circle"
              max-height="96"
              max-width="96"
              min-width="96"
              contain
              :src="avatarPaths[userStore.userData.avatar]"
            />
          </div>
        </v-col>
      </v-row>

      <v-row class="px-4 px-sm-16 mx-0">
        <v-col cols="12" class="d-flex flex-column">
          <p class="text-h4 font-weight-bold mb-1">{{ userStore.userData!.userName }}</p>
          <h3 class="text-h6 mb-1">
            {{ userStore.userData.firstName }} {{ userStore.userData.lastName }}
          </h3>
          <p class="mb-1">{{ userStore.userData.bio }}</p>
          <p class="text-body-1">Total Points: {{ userStore.userData!.totalPoints }} pts</p>
        </v-col>
      </v-row>

      <!-- Edit Profile Section -->
      <v-row class="px-4 px-sm-16 ml-3" no-gutters>
        <v-col cols="12">
          <p class="text-h6 font-weight-bold mb-2">Edit Profile (Avatar, Bio & Visibility)</p>
        </v-col>
        <v-col cols="12 mb-4">
          <v-btn
            class="bg-primaryBlue mb-4"
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
                <div class="d-flex flex-wrap gap-4 justify-center">
                  <v-img
                    v-for="(avatar, index) in avatarPaths"
                    :key="index"
                    :src="avatar"
                    max-height="96"
                    max-width="96"
                    min-width="96"
                    contain
                    class="rounded-circle cursor-pointer"
                    :class="{ 'border-primary': selectedAvatar === index }"
                    @click="selectedAvatar = index as 0 | 1 | 2 | 3 | 4 | 5"
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
                  :error-messages="bioError"
                  placeholder="Tell us about yourself!"
                  variant="outlined"
                  @focus="bioError = ''"
                  bg-color="rgb(var(--v-theme-primaryBrown))"
                />
              </v-col>
            </v-row>

            <!-- Visibility Section -->
            <v-row>
              <v-col cols="12">
                <p class="text-h6 font-weight-bold mb-4 justify-center">Visibility</p>
                <v-item-group mandatory class="d-flex flex-column" v-model="visibility">
                  <v-btn
                    v-for="(option, index) in visOptions"
                    :key="option"
                    :class="['mb-2', visibility === index ? 'bg-primaryGreen' : 'bg-primaryBrown']"
                    variant="outlined"
                    @click="visibility = index as 0 | 1 | 2"
                  >
                    {{ option }}
                  </v-btn>
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
                  :loading="loading"
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
