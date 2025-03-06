<script setup lang="ts">
import { ref } from 'vue'
import { useModalStore } from '@/stores/modal'
import type { ChallengeType, ChallengeStatus } from '@/types/challenge'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'
import FormData from 'form-data'
import type { BingoData } from '@/types/bingo'
import type { ExtendedAxiosError } from '@/types/other'

// Define interface for task submission
interface TaskSubmission {
  description: string
  image: File | null
  canShareOnSocialMedia: boolean
}

// Initialize modal store
const modalStore = useModalStore()
const messageStore = useMessageStore()
// Initialize task submission state
const taskSubmission = ref<TaskSubmission>({
  description: '',
  image: null,
  canShareOnSocialMedia: false,
})
const loading = ref(false)
const maxLength = (value: string) =>
  value.length <= 500 || 'The description can be at must 500 characters.'

// Define emits for component events
const emit = defineEmits<{
  (evt: 'close'): void
  (evt: 'start', index: number): void
  (evt: 'complete', bingoData: BingoData, index: number): void
}>()

// Define icons for different challenge types
const typeIcons = {
  connect: '/link.svg',
  understand: '/brain.svg',
  act: '/walking.svg',
}

// Define component props with imported types
const props = defineProps<{
  title: string
  points: number
  type: ChallengeType
  description: string
  status: ChallengeStatus
  isLoggedIn: boolean
  position: number
}>()

// Handle opening login modal
const openLoginModal = () => {
  modalStore.openLogin()
}

// Handle card close
const closeCard = () => {
  emit('close')
}

// Handle task start
const startTask = () => {
  if (!props.isLoggedIn) {
    return
  }
  loading.value = true
  server
    .post('/start-challenge/', { position: props.position })
    .then(() => emit('start', props.position))
    .catch((error: ExtendedAxiosError) => {
      messageStore.handleUnexpectedError(error.config?.session_expired, false)
    })
    .finally(() => (loading.value = false))
}

// Handle image upload
const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    taskSubmission.value.image = file
  }
}

// Handle task finish
const finish = () => {
  if (!taskSubmission.value.image) {
    messageStore.showMessage('Warning', 'You must upload an image', 'warning')
    return
  }
  if (taskSubmission.value.image.size >= 5 * 1024 * 1024) {
    messageStore.showMessage('Warning', 'Uploaded images can be at most 5MB', 'warning')
    return
  }
  if (maxLength(taskSubmission.value.description) !== true) {
    // don't allow submission if description is too long
    messageStore.showMessage(
      'Warning',
      'Your description can have at most 500 characters',
      'warning',
    )
    return
  }
  const data = new FormData()
  data.append('image', taskSubmission.value.image, taskSubmission.value.image?.name)
  data.append('position', props.position)
  data.append('consent', taskSubmission.value.canShareOnSocialMedia)
  data.append('description', taskSubmission.value.description)
  loading.value = true
  server
    .patch('/complete-challenge/', data, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'multipart/form-data; boundary=${data._boundary}',
      },
      timeout: 0,
    })
    .then((response) => {
      emit('complete', response.data as BingoData, props.position)
      taskSubmission.value.description = ''
      taskSubmission.value.image = null
      taskSubmission.value.canShareOnSocialMedia = false
    })
    .catch((error: ExtendedAxiosError) => {
      let unhandled = true
      if (error.response?.status === 400) {
        const validationErrors = error.response?.data as { image?: [string, ...string[]] }
        if (validationErrors.image) {
          unhandled = false
          if (validationErrors.image[0].startsWith('Upload a valid image')) {
            messageStore.showMessage('Invalid Image', 'Please upload an image file.', 'warning')
          } else {
            messageStore.showMessage('Invalid Image', validationErrors.image[0], 'warning')
          }
        }
      } else if (error.response?.status === 413) {
        unhandled = false
        messageStore.showMessage(
          'Invalid Image',
          'The image you uploaded is too large. Please upload an image less than 5MB.',
          'warning',
        )
      }
      if (unhandled) {
        messageStore.handleUnexpectedError(error.config?.session_expired, false)
      }
    })
    .finally(() => (loading.value = false))
}
</script>

<template>
  <div :class="['challenge-card-wrapper']">
    <v-card color="primaryBlue" rounded class="challenge-card">
      <div class="header">
        <div class="headerIcon" style="display: flex; flex-direction: column">
          <img :src="typeIcons[type]" :alt="`${type} icon`" />
          <p>{{ type }}</p>
        </div>
        <div class="header-content">
          <v-card-title>{{ title }}</v-card-title>
        </div>
        <v-icon icon="mdi-close-circle-outline" @click="closeCard" />
      </div>

      <v-card-subtitle style="font-weight: bold">
        <div class="points">{{ points }} Points</div>
      </v-card-subtitle>

      <template v-if="status === 'not started'">
        <div class="description">
          <v-card-text>{{ description }}</v-card-text>
        </div>
        <div class="button-container">
          <v-btn v-if="!isLoggedIn" @click="openLoginModal" class="action-button bg-primaryGreen"
            >Login</v-btn
          >
          <v-btn v-else @click="startTask" class="action-button bg-primaryGreen" :loading="loading"
            >Start</v-btn
          >
        </div>
      </template>

      <template v-else-if="status === 'started'">
        <div class="description">
          <v-checkbox
            v-model="taskSubmission.canShareOnSocialMedia"
            hide-details
            label="I consent for my submission to be posted on social media"
          />
          <div class="submission-area">
            <v-textarea
              v-model="taskSubmission.description"
              placeholder="Description"
              class="custom-textarea"
              variant="plain"
              no-resize
              :rules="[maxLength]"
            />
            <div class="d-flex">
              <div v-if="taskSubmission.image" class="mb-2 ml-2 file-preview">
                <img src="/FileIcon.svg" alt="File icon" class="file-icon" />
                <p class="file-name">{{ taskSubmission.image.name }}</p>
              </div>
              <v-spacer />
              <div class="mx-2 mt-6">
                <input
                  type="file"
                  id="file"
                  @change="handleImageUpload"
                  class="hidden-input"
                  accept="image/*"
                />
                <label for="file">
                  <img src="/Upload.svg" alt="Upload icon" class="upload-icon" />
                </label>
              </div>
            </div>
          </div>

          <div class="button-container">
            <v-btn @click="finish" class="action-button bg-primaryGreen" :loading="loading"
              >Finish</v-btn
            >
          </div>
        </div>
      </template>

      <template v-else>
        <div class="description">
          <v-card-text>{{ description }}</v-card-text>
        </div>
        <div class="button-container">
          <v-btn @click="closeCard" class="action-button" color="lightBlue" text-color="white"
            >Completed</v-btn
          >
        </div>
      </template>
    </v-card>
  </div>
</template>

<style scoped>
/* Card wrapper base styles */

/* Main card container */
.challenge-card {
  color: white;
  padding: 24px;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 16px;
  font-family: 'Poppins', sans-serif;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

/* Header section styles */
.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 8px;
  position: relative;
  width: 100%;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 200px;
  margin: 0 auto;
}

.v-card-title {
  color: white;
  font-size: 24px;
  line-height: 1.3;
  text-align: center;
  margin: 0;
  padding: 0;
  white-space: normal;
  overflow: visible;
  text-overflow: clip;
  font-weight: bold;
  font-family: 'Poppins', sans-serif;
}

.header img {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

/* Points display */
.points {
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  margin: 4px 0 20px;
}

/* Text content styles */
.v-card-text {
  color: white;
  text-align: center;
  padding: 0;
  margin-bottom: 8px;
  font-size: 16px;
  line-height: 1.5;
  font-family: 'Poppins', sans-serif;
}

.description {
  margin: 0;
  padding: 0 16px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Button container and styles */
.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 20px 0;
}

.action-button {
  font-family: 'Poppins', sans-serif;
  border-radius: 50px;
  min-width: 180px;
  height: 50px;
  font-size: 18px;
  text-transform: none;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: normal;
  padding: 0 32px;
}

/* Submission area styles */
.submission-area {
  position: relative;
  background-color: rgb(var(--v-theme-primaryBrown));
  border-radius: 12px;
  padding: 0;
  margin: 20px auto;
  min-height: 200px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.custom-textarea {
  background-color: transparent;
  border: none;
  outline: none;
  box-shadow: none;
  padding: 12px;
  min-height: 120px;
  color: rgb(var(--v-theme-primaryBlue));
  width: 100%;

  overflow-y: auto;
  font-family: 'Poppins', sans-serif;
}

.custom-textarea :deep(.v-field),
.custom-textarea :deep(.v-field__field) {
  background-color: transparent;
  border: none;
  outline: none;
  box-shadow: none;
}

/* Upload section styles */
.upload-icon {
  width: 28px;
  height: 28px;
  cursor: pointer;
}

.upload-icon:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.hidden-input {
  display: none;
}

.file-icon {
  width: 32px;
  height: 32px;
}

.file-name {
  color: rgb(var(--v-theme-primaryBlue));
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Poppins', sans-serif;
}

.file-preview {
  min-width: 0;
}

/* Mobile responsive styles */
@media (max-width: 600px) {
  .challenge-card {
    width: 100%;
    padding: 16px;
    margin: 0;
    border-radius: 12px;
  }

  .header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    padding-top: 12px;
    margin-bottom: 12px;
    gap: 4px;
  }

  .header img {
    width: 48px;
    height: 48px;
  }

  .v-card-title {
    font-size: 20px;
  }

  .header-content {
    max-width: 160px;
  }

  .points {
    font-size: 14px;
    margin: 4px 0 16px;
  }

  .description {
    padding: 0 8px;
  }

  .v-card-text {
    font-size: 14px;
  }

  .v-icon {
    position: absolute;
    top: 16px;
    right: 16px;
  }

  .submission-area {
    width: 100%;
    margin: 12px auto;
    min-height: 180px;
  }

  .custom-textarea {
    padding: 8px;
    min-height: 100px;
    font-size: 14px;
  }

  .file-name {
    font-size: 11px;
  }

  .action-button {
    font-size: 16px;
    min-width: 160px;
    height: 45px;
  }
}

/* Touch device styles */
@media (hover: none) {
  .upload-icon:hover {
    background-color: transparent;
  }
}
</style>
