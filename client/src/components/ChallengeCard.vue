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
      <v-icon icon="mdi-close-circle-outline" class="mr-3 mt-3" @click="closeCard"></v-icon>
      <v-card-title style="font-weight: bold">Watch an Ocean Documentary</v-card-title>
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
      <v-btn color="pink" @click="startTask">Start</v-btn>
    </v-card-actions>
  </v-card>

  <v-card v-else-if="isStarted && !isCompleted" color="primaryBlue" rounded>
    <div class="header">
      <img src="../assets/BrainIcon.svg" alt="Brain icon" />
      <v-icon icon="mdi-close-circle-outline" class="mr-3 mt-3" @click="closeCard"></v-icon>
      <v-card-title style="font-weight: bold">Watch an Ocean Documentary</v-card-title>
    </div>
    <v-card-subtitle style="font-weight: bold">
      <div class="points">200 Points</div>
    </v-card-subtitle>
    <v-checkbox
      v-model="taskSubmission.canShareOnSocialMedia"
      label="Can Blue Crew use this image on Social Media?"
    ></v-checkbox>
    <div class="content">
      <v-textarea v-model="taskSubmission.feedback" label="Feedback" rows="5"></v-textarea>

      <input
        type="file"
        ref="fileInput"
        @change="handleImageUpload"
        accept="image/*"
        style="display: none"
      />
      <div class="upload-icon" @click="$refs.fileInput.click()">
        <v-icon icon="mdi-file-document-outline"></v-icon>
        <span class="file-text">{{ taskSubmission.image?.name || 'my_imag...' }}</span>
      </div>

      <v-card-actions>
        <v-btn @click="finish">Finish</v-btn>
      </v-card-actions>
    </div>
  </v-card>

  <v-card v-else color="primaryBlue" rounded>
    <div class="header">
      <img src="../assets/BrainIcon.svg" alt="Brain icon" />
      <v-icon icon="mdi-close-circle-outline" class="mr-3 mt-3" @click="closeCard"></v-icon>
      <v-card-title style="font-weight: bold">Watch an Ocean Documentary</v-card-title>
    </div>
    <v-card-subtitle style="font-weight: bold">
      <div class="points">200 Points</div>
    </v-card-subtitle>

    <v-card-text>
      Here are some of our top picks! You can choose one of them or watch one of your own. Tell us
      what you thought and submit a picture.
      <ul>
        <li>David Attenborough, Our Planet Coastal Seas</li>
        <li>Cleaning up the Ocean</li>
      </ul>
    </v-card-text>
    <v-card-actions>
      <v-btn color="blue" disabled>Completed</v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped></style>
