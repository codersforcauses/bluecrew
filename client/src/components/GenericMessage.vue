<template>
    <v-snackbar
      :model-value="visible"
      :color="color"
      timeout="3000"
      top
      @update:model-value="close"
    >
      <div class="message-content">
        <h3 class="message-title">{{ title }}</h3>
        <p class="message-text">{{ text }}</p>
      </div>
      <v-btn class="close-btn" @click="close" variant="text">CLOSE</v-btn>
    </v-snackbar>
  </template>


<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  title: String,
  text: String,
  type: {
    type: String,
    default: 'success',
    validator: (value: string) => ['success', 'warning', 'error'].includes(value),
  },
})

const emit = defineEmits(['update:visible'])

const colorMapping: Record<string, string> = {
  success: 'green',
  warning: 'amber',
  error: 'red',
}

const color = computed(() => colorMapping[props.type] || 'green')

const close = () => {
  emit('update:visible', false)
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
  }
  
  .message-text {
    font-size: 16px;
    margin: 0;
    margin-top: 4px; 
  }
  
  .close-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 14px;
    text-transform: uppercase;
    font-weight: bold;
    color: white;
    background: none;
    border: none;
  }
  </style>
  