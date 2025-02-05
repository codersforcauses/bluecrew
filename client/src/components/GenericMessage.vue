<template>
  <v-snackbar
    :model-value="store.isOpen"
    :color="color"
    timeout="3000"
    top
    @update:model-value="close"
  >
    <div class="message-content">
      <h3 class="message-title">{{ store.title }}</h3>
      <p class="message-text">{{ store.content }}</p>
    </div>
    <template v-slot:actions>
      <v-btn class="close-btn" @click="close" variant="text">CLOSE</v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMessageStore } from '@/stores/message'

const store = useMessageStore()

const colorMapping: Record<string, string> = {
  success: 'green',
  warning: 'amber',
  error: 'red',
}

const color = computed(() => colorMapping[store.type])

const close = () => {
  store.closeMessage()
}
</script>

<style scoped>
.message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding-right: 3rem;
}

.message-title {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
  color: white;
}

.message-text {
  font-size: 16px;
  margin: 0;
  margin-top: 4px;
  color: white;
}

.close-btn {
  position: absolute;
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  font-size: 14px;
  text-transform: uppercase;
  font-weight: bold;
  color: white;
  background: none;
  border: none;
}
</style>
