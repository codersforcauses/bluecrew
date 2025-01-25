<script setup lang="ts">
import { ref } from 'vue'
import { useModalStore } from '@/stores/modal'

interface TaskSubmission {
  feedback: string
  image: File | null
  canShareOnSocialMedia: boolean
}

const modalStore = useModalStore()

const openLoginModal = () => {
  modalStore.openLogin()
}
const taskSubmission = ref<TaskSubmission>({
  feedback: '',
  image: null,
  canShareOnSocialMedia: false,
})

const emit = defineEmits<{
  (evt: 'close'): void
  (evt: 'status-change', status: 'not started' | 'started' | 'completed'): void
  (evt: 'task-completed', submission: TaskSubmission): void
}>()

const typeIcons = {
  connect: '/link.svg', // Maybe a network/connection brain icon
  understand: '/brain.svg', // Perhaps a brain with a lightbulb
  act: '/walking.svg', // A brain with a rocket or action symbol
}
// Define props
const props = defineProps<{
  title: string
  points: number
  type: 'connect' | 'understand' | 'act'
  description: string
  status: 'not started' | 'started' | 'completed'
  isLoggedIn: boolean
}>()

const closeCard = () => {
  emit('close')
}

const startTask = () => {
  if (!props.isLoggedIn) {
    return
  }
  emit('status-change', 'started')
}

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    taskSubmission.value.image = file
  }
}

const finish = () => {
  if (!taskSubmission.value.feedback && !taskSubmission.value.image) {
    alert('Please provide feedback or upload an image')
    return
  }
  emit('task-completed', taskSubmission.value)
  emit('status-change', 'completed')
}
</script>

<template>
  <v-card color="primaryBlue" rounded>
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
      <v-card-actions>
        <v-btn color="white" v-if="!isLoggedIn" @click="openLoginModal">Login in</v-btn>
        <v-btn color="white" v-else @click="startTask">Start</v-btn>
      </v-card-actions>
    </template>

    <!-- Started Content -->
    <template v-else-if="status === 'started'">
      <div class="description">
        <div class="submission-area" width="95%">
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

        <div class="finish-button-wrapper">
          <v-btn @click="finish" class="finish-button">Finish</v-btn>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="description">
        <v-card-text>{{ description }}</v-card-text>
      </div>
      <v-card-actions>
        <v-btn @click="closeCard" class="completed-btn">Completed</v-btn>
      </v-card-actions>
    </template>
  </v-card>
</template>

<style scoped>
.v-card {
  color: white;
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

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
}

.header img {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.points {
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  margin: 4px 0 20px;
}

.v-card-text {
  color: white;
  text-align: center;
  padding: 0;
  margin-bottom: 8px;
  font-size: 16px;
  line-height: 1.5;
}

ul {
  list-style-type: disc;
  padding: 0;
  margin: 0px 0;
  text-align: center;
}

li {
  margin: 8px 0;
  color: white;
  font-size: 16px;
}

.v-card-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 20px;
  margin: 0 auto;
}

.v-btn {
  background-color: rgb(var(--v-theme-primaryPink));
  color: rgb(var(--v-theme-primaryWhite));
  justify-content: center;
}

.description {
  text-align: center;
  margin: 0;
  padding: 0 16px;
}

.v-textarea {
  background-color: rgb(var(--v-theme-primaryBrown));
  --v-field-border-width: 0;
  box-shadow: none;
  padding: 12px;
  min-height: 120px;
  color: rgb(var(--v-theme-primaryBlue));
  width: 95%;
  border: none;
}
.upload-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.upload-icon:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.v-checkbox :deep(.v-label) {
  color: rgb(var(--v-theme-primaryWhite));
  opacity: 0.9;
}
.completed-btn {
  background-color: rgb(var(--v-theme-lightBlue));
}
.hidden-input {
  display: none;
}

.submission-area {
  position: relative;
  background-color: rgb(var(--v-theme-primaryBrown));
  border-radius: 12px;
  padding: 0px;
  margin: 20px auto;
  min-height: 200px;
  width: 90%;
}

.custom-textarea :deep(.v-field),
.custom-textarea :deep(.v-field__field) {
  background-color: transparent;
  border: none;
  outline: none;
  box-shadow: none;
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
  white-space: nowrap; /* Prevent text wrapping */
  max-width: 84px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.upload-button-wrapper {
  position: absolute;
  bottom: 20px;
  right: 20px;
}

.finish-button-wrapper {
  text-align: center;
  margin-top: -30px; /* Adjust the button position */
}

.finish-button {
  background-color: rgb(var(--v-theme-primaryPink));
  color: white;
  padding: 8px 24px;
  border-radius: 20px;
}
/* Mobile styles - Apply when screen width is 600px or less */
@media (max-width: 600px) {
  .v-card {
    padding: 16px;
    max-width: 100%;
    margin: 0 8px;
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
    font-weight: bold;
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
  li {
    font-size: 14px;
    margin: 6px 0;
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

  /* Adjust the upload and file preview area for better touch targets */
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

  /* Make the finish button more touch-friendly */
  .finish-button-wrapper {
    margin-top: -24px;
  }

  .finish-button {
    width: 80%; /* Make button wider on mobile */
    padding: 12px 20px;
    font-size: 16px;
  }

  /* Adjust checkbox for mobile */
  .v-checkbox {
    margin: 8px 0;
  }

  .v-checkbox :deep(.v-label) {
    font-size: 14px;
  }
}

/* Add touch-friendly hover states for mobile */
@media (hover: none) {
  .upload-icon:hover {
    background-color: transparent;
  }

  .v-btn:hover {
    opacity: 1;
  }
}
</style>
