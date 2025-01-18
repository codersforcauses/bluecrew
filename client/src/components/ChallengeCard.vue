<script setup lang="ts">
import { ref } from 'vue'

interface TaskSubmission {
  feedback: string
  image: File | null
  canShareOnSocialMedia: boolean
}

const taskSubmission = ref<TaskSubmission>({
  feedback: '',
  image: null,
  canShareOnSocialMedia: false,
})
const isStarted = ref(false)
const isCompleted = ref(false)
const emit = defineEmits<{
  (evt: 'close'): void
  (evt: 'task-completed', submission: TaskSubmission): void
}>()

const closeCard = () => {
  emit('close')
}

const startTask = () => {
  isStarted.value = true
}

const completeTask = () => {
  isCompleted.value = true
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
  completeTask()
  emit('task-completed', taskSubmission.value)
}
</script>

<template>
  <v-card v-if="!isStarted && !isCompleted" color="primaryBlue" rounded>
    <div class="header">
      <img src="../assets/BrainIcon.svg" alt="Brain icon" />
      <div class="header-content">
        <v-card-title>Watch an Ocean Documentary</v-card-title>
      </div>
      <v-icon icon="mdi-close-circle-outline" @click="closeCard"></v-icon>
    </div>
    <v-card-subtitle style="font-weight: bold">
      <div class="points">200 Points</div></v-card-subtitle
    >

    <div class="description">
      <v-card-text
        >Here are some of our top picks! You can choose one of them or watch one of your own.Tell us
        what you thought and submit a picture.</v-card-text
      >
      <ul>
        <li>David Attenborough, Our Planet Coastal Seas</li>
        <li>Cleaning up the Ocean</li>
      </ul>
    </div>
    <v-card-actions>
      <v-btn color="white" @click="startTask">Start</v-btn>
    </v-card-actions>
  </v-card>

  <v-card v-else-if="isStarted && !isCompleted" color="primaryBlue" rounded>
    <div class="header">
      <img src="../assets/BrainIcon.svg" alt="Brain icon" />
      <div class="header-content">
        <v-card-title>Watch an Ocean Documentary</v-card-title>
      </div>
      <v-icon icon="mdi-close-circle-outline" @click="closeCard"></v-icon>
    </div>
    <v-card-subtitle style="font-weight: bold">
      <div class="points">200 Points</div>
      <v-checkbox
        v-model="taskSubmission.canShareOnSocialMedia"
        label="Can Blue Crew use this image on Social Media?"
      ></v-checkbox>
    </v-card-subtitle>

    <div class="description">
      <v-textarea v-model="taskSubmission.feedback" placeholder="Feedback"></v-textarea>

      <div class="file-upload-container">
        <!-- 上传的文件预览和文件名 -->
        <div class="file-preview">
          <div v-if="taskSubmission.image" class="file-info">
            <img src="../assets/FileIcon.svg" alt="File icon" class="file-icon" />
            <span class="file-name">{{ taskSubmission.image.name }}</span>
          </div>
        </div>

        <!-- 上传按钮 -->
        <div class="upload-button-wrapper">
          <input type="file" id="file" @change="handleImageUpload" class="hidden-input" />
          <label for="file" class="upload-button">
            <img src="../assets/Upload.svg" alt="Upload icon" class="upload-icon" />
          </label>
        </div>
      </div>

      <v-card-actions>
        <v-btn @click="finish">Finish</v-btn>
      </v-card-actions>
    </div>
  </v-card>

  <v-card v-else color="primaryBlue" rounded>
    <div class="header">
      <img src="../assets/BrainIcon.svg" alt="Brain icon" />
      <div class="header-content">
        <v-card-title>Watch an Ocean Documentary</v-card-title>
      </div>
      <v-icon icon="mdi-close-circle-outline" @click="closeCard"></v-icon>
    </div>
    <v-card-subtitle style="font-weight: bold">
      <div class="points">200 Points</div>
    </v-card-subtitle>
    <div class="description">
      <v-card-text>
        Here are some of our top picks! You can choose one of them or watch one of your own. Tell us
        what you thought and submit a picture.
        <ul>
          <li>David Attenborough, Our Planet Coastal Seas</li>
          <li>Cleaning up the Ocean</li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="closeCard" color="primary-white" class="completed-btn">Completed</v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>

<style scoped>
.v-card {
  background-color: primaryBlue !important;
  color: white !important;
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px !important;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
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
  color: white !important;
  font-size: 24px !important;
  line-height: 1.3;
  text-align: center;
  margin: 0 !important;
  padding: 0 !important;
  white-space: normal !important;
  overflow: visible !important; /* 允许内容溢出 */
  text-overflow: clip !important; /* 不使用省略号 */
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
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
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
  border: none !important; /* 移除边框 */
  outline: none !important; /* 移除轮廓 */
  box-shadow: none !important;
  padding: 12px;
  min-height: 120px;
  color: rgb(var(--v-theme-primaryBlue));
  width: 95%;
}

.upload-icon {
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px dashed rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
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
.description {
  width: 90%;
  justify-content: center;
  align-items: center;
  display: flex; /* Add this */
  flex-direction: column;
  margin: 0 auto;
}
</style>
