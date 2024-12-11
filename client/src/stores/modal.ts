import { ref } from 'vue'
import { defineStore } from 'pinia'

type ModalType = 'login' | 'register' | 'none'

export const useModalStore = defineStore('modal', () => {
  const currentModal = ref<ModalType>('none')

  function openRegister() {
    currentModal.value = 'register'
  }

  function openLogin() {
    currentModal.value = 'login'
  }

  function closeModal() {
    currentModal.value = 'none'
  }

  return {
    currentModal,
    openRegister,
    openLogin,
    closeModal,
  }
})
