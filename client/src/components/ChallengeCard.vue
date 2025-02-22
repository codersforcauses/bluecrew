<script setup lang="ts">
import { ref } from 'vue'
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'
import type { ChallengeType, ChallengeStatus } from '@/types/challenge'
import server from '@/utils/server'
import { useMessageStore } from '@/stores/message'
import FormData from 'form-data'

const { mobile } = useDisplay()

// Define interface for task submission
interface TaskSubmission {
  feedback: string
  image: File | null
  canShareOnSocialMedia: boolean
}

// Initialize modal store
const modalStore = useModalStore()
const messageStore = useMessageStore()
// Initialize task submission state
const taskSubmission = ref<TaskSubmission>({
  feedback: '',
  image: null,
  canShareOnSocialMedia: false,
})

// Define emits for component events
const emit = defineEmits<{
  (evt: 'close'): void
  (evt: 'status-change', status: ChallengeStatus): void
  (evt: 'task-completed', submission: TaskSubmission): void
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
  server
    .post('/start-challenge/', { position: props.position })
    .then(() => emit('status-change', 'started'))
    .catch(() => {
      messageStore.showMessage(
        'Error',
        'Unexpected occured while attempting to start challenge.',
        'error',
      )
    })
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
  if (!taskSubmission.value.feedback && !taskSubmission.value.image) {
    messageStore.showMessage('Warning', 'Please provide feedback or upload an image', 'warning')
    return
  }
  const data = new FormData()
  data.append('image', taskSubmission.value.image, taskSubmission.value.image?.name)
  data.append('position', props.position)
  data.append('consent', taskSubmission.value.canShareOnSocialMedia)
  data.append('description', taskSubmission.value.feedback)
  server
    .patch('/complete-challenge/', data, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'multipart/form-data; boundary=${data._boundary}',
      },
    })
    .then(() => {
      emit('task-completed', taskSubmission.value)
      emit('status-change', 'completed')
      taskSubmission.value.feedback = ''
      taskSubmission.value.image = null
      taskSubmission.value.canShareOnSocialMedia = false
      //   TODO consent field doesn't exist
    })
    .catch(() =>
      messageStore.showMessage(
        'Error',
        'Unexpected occured while attempting to complete challenge.',
        'error',
      ),
    )
}
</script>

<template>
  <div :class="['challenge-card-wrapper', { mobile: mobile }]">
    <div v-if="mobile" class="overlay"></div>
    <v-card color="primaryBlue" rounded class="challenge-card">
      <div class="header">
        <div class="headerIcon" style="display: flex; flex-direction: column">
          <img :src="typeIcons[type]" :alt="`${type} icon`" />
          <p>{{ type }}</p>
        </div>
        <div class="header-content">
          <v-card-title>{{ title }}</v-card-title>
        </div>
        <v-icon icon="mdi-close-circle-outline" @click="closeCard"></v-icon>
      </div>

      <v-card-subtitle style="font-weight: bold">
        <div class="points">{{ points }} Points</div>
      </v-card-subtitle>

      <template v-if="status === 'not started'">
        <div class="description">
          <v-card-text>{{ description }}</v-card-text>
        </div>
        <div class="button-container">
          <v-btn v-if="!isLoggedIn" @click="openLoginModal" class="action-button">Login</v-btn>
          <v-btn v-else @click="startTask" class="action-button">Start</v-btn>
        </div>
      </template>

      <template v-else-if="status === 'started'">
        <div class="description">
          <div class="submission-area">
            <v-textarea
              v-model="taskSubmission.feedback"
              placeholder="Feedback"
              class="custom-textarea"
              variant="plain"
            ></v-textarea>

            <div class="file-preview" v-if="taskSubmission.image">
              <img src="/FileIcon.svg" alt="File icon" class="file-icon" />
              <span class="file-name">{{ taskSubmission.image.name }}</span>
            </div>

            <div class="upload-button-wrapper">
              <input type="file" id="file" @change="handleImageUpload" class="hidden-input" />
              <label for="file">
                <img src="/Upload.svg" alt="Upload icon" class="upload-icon" />
              </label>
            </div>
          </div>

          <div class="button-container">
            <v-btn @click="finish" class="action-button">Finish</v-btn>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="description">
          <v-card-text>{{ description }}</v-card-text>
        </div>
        <div class="button-container">
          <v-btn @click="closeCard" class="action-button completed-btn">Completed</v-btn>
        </div>
      </template>
    </v-card>
  </div>
</template>

<style scoped>
/* Card wrapper base styles */
.challenge-card-wrapper {
  width: 100%;
  margin: 1rem 0;
}

/* Mobile specific styles */
.challenge-card-wrapper.mobile {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

/* Overlay only shows on mobile */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

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

.mobile .challenge-card {
  z-index: 1001;
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
  text-align: center;
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
  background-color: #007d85 !important;
  color: white !important;
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

.action-button.completed-btn {
  background-color: #3fbee0 !important;
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
  resize: none;
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
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.upload-icon:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.hidden-input {
  display: none;
}

.file-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  position: absolute;
  bottom: 20px;
  left: 20px;
}

.file-icon {
  width: 32px;
  height: 32px;
}

.file-name {
  color: rgb(var(--v-theme-primaryBlue));
  font-size: 12px;
  text-align: center;
  white-space: nowrap;
  max-width: 84px;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Poppins', sans-serif;
}

.upload-button-wrapper {
  position: absolute;
  bottom: 20px;
  right: 20px;
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

  .file-preview {
    bottom: 16px;
    left: 16px;
  }

  .file-icon {
    width: 28px;
    height: 28px;
  }

  .file-name {
    font-size: 11px;
    max-width: 42px;
  }

  .upload-button-wrapper {
    bottom: 16px;
    right: 16px;
  }

  .upload-icon {
    width: 28px;
    height: 28px;
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
