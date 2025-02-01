import { defineStore } from 'pinia'

export const useMessageStore = defineStore ('message', {
    state: (): Message => ({
        isOpen: false,
        content: '',
    }),

    actions: {
        showMessage(message: string) {
            this.content = message
            this.isOpen = true
        },

        closeMessage() {
            this.isOpen = false
            this.content = ''
        }
    }
})

interface Message {
    isOpen: boolean
    content: string
  }