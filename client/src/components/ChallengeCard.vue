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
  close: () => void
  'task-completed': (submission: TaskSubmission) => void
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
  emit('task-completed', taskSubmission.value)
}
</script>
<template>
  <v-card
  color="primaryBlue"
  rounded="xl"
  width="500px"
  >
    <div class="header">
      <button class="close-button">x</button>
      <v-card-title style="font-weight: bold;">Watch an Ocean Documentary</v-card-title>
    </div>
    <v-card-subtitle class="points" style="font-weight: bold;"> 200 Points</v-card-subtitle>

    <div class="description">
      <v-card-text style="font-weight: bold;">
        Here are some of our top picks! You can choose one of them or watch one of your own. Tell us
        what you thought and submit a picture.
        <br> David Attenborough, Our Planet Coastal Seas
        <br> Cleaning up the Ocean
      </v-card-text>
    </div>
    <v-action>
      <v-btn>Start</v-btn>
    </v-action>
  </v-card>
</template>

<style scoped>
</style>
