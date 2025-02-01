import { defineStore } from 'pinia'
import { ref } from 'vue'

export type MessageType = 'success' | 'warning' | 'error'

export const useMessageStore = defineStore('message', () => {
  const isOpen = ref(false)
  const content = ref('')
  const title = ref('')
  const type = ref<MessageType>('success')

  function showMessage(message: string, messageTitle: string, messageType: MessageType = 'success') {
    isOpen.value = true
    content.value = message
    title.value = messageTitle 
    type.value = messageType
  }

  function closeMessage() {
    isOpen.value = false
    content.value = ''
    title.value = ''
  }

  return {
    isOpen,
    content,
    title,
    type,
    showMessage,
    closeMessage
  }
})