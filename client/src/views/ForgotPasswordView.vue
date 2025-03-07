<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMessageStore } from '@/stores/message'
import { useUserStore } from '@/stores/user'
import { useModalStore } from '@/stores/modal'
import router from '@/router'
import ErrorCorrectionRequest from '@/components/ErrorCorrectionRequest.vue'

const props = defineProps<{ token?: string; uid?: string }>()
const messageStore = useMessageStore()
const userStore = useUserStore()
const modalStore = useModalStore()
const isValid = ref(false)
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const passwordErrors = ref('')
const formSubmissionAttempted = ref(false)
const required = (value: string) => !!value || 'Required.'
const passwordsMatch = (value: string) => value === password.value || 'Passwords do not match.'
const paramsInvalid = ref(false)

const resetPassword = async () => {
  formSubmissionAttempted.value = true
  if (!isValid.value) {
    return
  }
  if (props.token && props.uid) {
    loading.value = true
    const resetResult = await userStore.resetPassword(password.value, props.uid, props.token)
    if (resetResult === true) {
      messageStore.showMessage('Success', 'Password has been reset', 'success')
      router.replace('/')
      modalStore.openLogin()
    } else if (resetResult === false) {
      messageStore.handleUnexpectedError(undefined, false)
    } else if (resetResult === 'invalid link') {
      paramsInvalid.value = true
      messageStore.showMessage('Error', 'Invalid password reset link', 'error')
    } else {
      passwordErrors.value = resetResult[0]
    }
    loading.value = false
  } else {
    messageStore.showMessage('Error', 'Invalid password reset link', 'error')
  }
}

onMounted(() => {
  if (!props.token || !props.uid) {
    paramsInvalid.value = true
    messageStore.showMessage('Error', 'Invalid password reset link', 'error')
  }
})
</script>
<template>
  <div class="reset-password-container">
    <div class="reset-password">
      <h2 class="text-primaryGreen">Reset Password</h2>
      <p class="text-primaryGreen">Enter your new password below.</p>
      <v-form v-model="isValid" @submit.prevent="resetPassword" validate-on="invalid-input">
        <div class="input-group">
          <label class="text-primaryGreen" for="password">New Password</label>
          <v-text-field
            class="mt-2"
            bg-color="primaryBrown"
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter new password"
            variant="outlined"
            :rules="[required]"
            :error-messages="passwordErrors"
            @focus="passwordErrors = ''"
            clearable
          />
        </div>

        <div class="input-group">
          <label class="text-primaryGreen" for="confirmPassword">Confirm Password</label>
          <v-text-field
            class="mt-2"
            bg-color="primaryBrown"
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            placeholder="Confirm new password"
            :rules="[required, passwordsMatch]"
            variant="outlined"
            clearable
          />
        </div>

        <v-btn
          class="d-flex justify-center mt-8 w-50 mx-auto"
          color="primaryBlue"
          height="50px"
          font-family="Lilita One, cursive"
          rounded
          type="submit"
          :loading="loading"
          >Reset Password</v-btn
        >
        <ErrorCorrectionRequest v-if="formSubmissionAttempted && !isValid" />
      </v-form>
    </div>
  </div>
</template>

<style scoped>
.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  overflow: hidden;
}

h2 {
  font-family: 'Lilita One', cursive;
  font-size: 40px;
}

p {
  font-family: 'Poppins';
  font-size: 18px;
  font-weight: bold;
}

.reset-password {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  text-align: center;
}

.reset-password h2,
.reset-password p,
.reset-password .input-group,
.reset-password .v-btn,
.reset-password .message {
  margin-bottom: 20px;
  /* Adjust the spacing as needed */
}

.input-group {
  text-align: left;
  font-family: 'Poppins';
  font-size: 18px;
  font-weight: bold;
}

.message {
  font-family: 'Poppins';
  font-size: 18px;
  font-weight: bold;
  color: red;
}
</style>
