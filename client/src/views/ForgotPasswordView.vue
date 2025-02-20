<script setup lang="ts">
import { defineProps, onMounted, ref } from 'vue'
import { useMessageStore } from '@/stores/message'
import { useUserStore } from '@/stores/user'

const props = defineProps<{ token?: string; uid?: string }>()
const messageStore = useMessageStore()
const userStore = useUserStore()
const isValid = ref(false)
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const passwordErrors = ref('')
const required = (value: string) => !!value || 'Required.'
const passwordsMatch = (value: string) => value === password.value || 'Passwords do not match.'
const paramsInvalid = ref(false)

const resetPassword = async () => {
  if (props.token && props.uid) {
    loading.value = true
    const resetResult = await userStore.resetPassword(password.value, props.uid, props.token)
    if (resetResult === true) {
      messageStore.showMessage('Success', 'Password has been reset', 'success')
    } else if (resetResult === false) {
      messageStore.showMessage(
        'Error',
        'An unexpected error occurred while trying to reset your password.',
        'error',
      )
    } else if (resetResult === 'invalid link') {
      paramsInvalid.value = true
      messageStore.showMessage('Error', 'Invalid password reset link', 'error')
    } else {
      passwordErrors.value = resetResult[0]
    }
    loading.value = false
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
      <v-form v-model="isValid" @submit.prevent="resetPassword" validate-on="blur">
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
          :disabled="!isValid || paramsInvalid"
          :loading="loading"
          >Reset Password</v-btn
        >
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
