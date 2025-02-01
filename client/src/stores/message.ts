import { defineStore } from 'pinia'
import { ref } from 'vue'

export type MessageType = 'success' | 'warning' | 'error'

export const useMessageStore = defineStore('message', () => {
  const isOpen = ref(false)
  const title = ref('')
  const content = ref('')
  const type = ref<MessageType>('success')

  function showMessage(
    messageTitle: string,
    message: string,
    messageType: MessageType = 'success',
  ) {
    isOpen.value = true
    title.value = messageTitle
    content.value = message
    type.value = messageType
  }

  function closeMessage() {
    isOpen.value = false
    title.value = ''
    content.value = ''
  }

  return {
    isOpen,
    title,
    content,
    type,
    showMessage,
    closeMessage,
  }
})
