<script setup lang="ts">
import { ref, computed } from 'vue'
import { useModalStore } from '@/stores/modal'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useMessageStore } from '@/stores/message'
import ErrorCorrectionRequest from './ErrorCorrectionRequest.vue'

const { xs } = useDisplay()
const modalStore = useModalStore()
const userStore = useUserStore()
const messageStore = useMessageStore()

const username = ref('')
const password = ref('')
const email = ref('')
const emailError = ref('')
const valid = ref(false)
const formSubmissionAttempted = ref(false)
const emailFormValid = ref(false)
const emailFormSubmissionAttempted = ref(false)
const loading = ref(false)

const currentPage = ref<'login' | 'forgot-password'>('login')

const setCurrentPage = (page: 'login' | 'forgot-password') => {
  currentPage.value = page
}
const required = (value: string) => !!value || 'Required.'
const emailProbablyValid = (value: string) => /^\S+@\S+\.\S+$/.test(value) || 'Invalid e-mail.'
const errorMessage = ref('')

const isDialogVisible = computed({
  get: () => modalStore.currentModal === 'login',
  set: (value: boolean) => {
    if (!value) {
      modalStore.closeModal()
    }
  },
})

const closeDialog = () => {
  modalStore.closeModal()
}

const openRegisterModal = () => {
  modalStore.openRegister()
}

const submitForm = async () => {
  formSubmissionAttempted.value = true
  if (valid.value) {
    loading.value = true
    const body = {
      username: username.value,
      password: password.value,
    }
    const loginResult = await userStore.login(body)
    if (loginResult === true) {
      messageStore.showMessage('Success', 'Login success.', 'success')
      closeDialog()
    } else if (loginResult === false) {
      messageStore.handleUnexpectedError(undefined, true)
    } else {
      errorMessage.value = 'No user with the given username and password was found.'
    }
    loading.value = false
  }
}

const requestPasswordReset = async () => {
  emailFormSubmissionAttempted.value = true
  if (emailFormValid.value) {
    loading.value = true
    const resetResult = await userStore.requestPasswordReset(email.value)
    if (resetResult === true) {
      messageStore.showMessage('Success', 'Reset link sent', 'success')
      closeDialog()
    } else if (resetResult === false) {
      messageStore.showMessage('Error', 'An unexpected error occured.', 'error')
    } else {
      emailError.value = resetResult
    }
    loading.value = false
  }
}
</script>

<template>
  <v-dialog
    v-model="isDialogVisible"
    :max-width="xs ? '100%' : '500px'"
    :fullscreen="xs"
    scrollable
    persistent
  >
    <v-card>
      <v-container>
        <v-row align="center">
          <template v-if="currentPage === 'forgot-password'">
            <button class="back-button" @click="setCurrentPage('login')">
              <v-icon icon="mdi-arrow-left" />
            </button>
          </template>
          <v-spacer />

          <button class="close-button" @click="closeDialog">
            <v-icon icon="mdi-close-circle-outline" />
          </button>
        </v-row>
      </v-container>

      <v-card-title class="d-flex justify-center">
        <img src="/blingo-logo.svg" alt="Blingo Logo" class="logo" />
      </v-card-title>

      <!-- Login Page -->
      <template v-if="currentPage === 'login'">
        <v-card-subtitle class="text-center subtitle mt-2 text-primaryGreen">
          <strong>
            <h3 style="font-family: 'Lilita One', cursive"><b>Welcome Back</b></h3>
          </strong>
        </v-card-subtitle>
        <v-card-text>
          <p class="text-center mb-4 text-primaryGreen" style="font-family: 'Lilita One', cursive">
            <b>Login to your existing account</b>
          </p>
          <v-form v-model="valid" validate-on="invalid-input" @submit.prevent="submitForm">
            <v-card-subtitle class="text-left subtitle mb-3 pa-0 text-primaryGreen">
              Username
            </v-card-subtitle>
            <v-text-field
              v-model="username"
              placeholder="Enter your username"
              hide-details="auto"
              :rules="[required]"
              outlined
              bg-color="primaryBrown"
              variant="outlined"
              :error-messages="errorMessage"
              @focus="errorMessage = ''"
            />
            <v-card-subtitle class="text-left subtitle mt-3 mb-3 pa-0 text-primaryGreen">
              Password
            </v-card-subtitle>
            <v-text-field
              v-model="password"
              placeholder="Enter your password"
              hide-details="auto"
              type="password"
              :rules="[required]"
              outlined
              bg-color="primaryBrown"
              variant="outlined"
              :error-messages="errorMessage"
              @focus="errorMessage = ''"
            />
            <div class="mt-3">
              <a
                class="text-subtitle-2 margin-left-adjust text-primaryGreen cursor-pointer"
                @click.prevent="setCurrentPage('forgot-password')"
                >Forgot Username or Password?
              </a>
            </div>
            <v-btn
              class="d-flex button-custom justify-center mt-4 w-50 mx-auto"
              color="primaryBlue"
              rounded
              elevation="12"
              type="submit"
              :loading="loading"
            >
              Sign In
            </v-btn>
            <ErrorCorrectionRequest v-if="formSubmissionAttempted && !valid" />
          </v-form>
        </v-card-text>
        <v-card-actions class="d-flex justify-center text-primaryGreen">
          <footer>
            Don't have an account?
            <a class="text-primaryGreen cursor-pointer" @click.prevent="openRegisterModal"
              >Sign up</a
            >
          </footer>
        </v-card-actions>
      </template>

      <!-- Forgot Password Page -->
      <template v-if="currentPage === 'forgot-password'">
        <v-card-subtitle class="text-center subtitle mt-2 text-primaryGreen">
          <strong>
            <h3><b>Forgot Username or Password</b></h3>
          </strong>
        </v-card-subtitle>
        <v-card-text>
          <v-form
            v-model="emailFormValid"
            @submit.prevent="requestPasswordReset"
            validate-on="invalid-input"
          >
            <p class="text-center">Enter your email below and we'll send you a reset link.</p>
            <v-text-field
              v-model="email"
              placeholder="Enter your email"
              hide-details="auto"
              required
              outlined
              bg-color="primaryBrown"
              variant="outlined"
              type="email"
              :rules="[required, emailProbablyValid]"
              :error-messages="emailError"
              @focus="emailError = ''"
            />

            <v-btn
              class="d-flex justify-center mt-8 w-50 mx-auto"
              color="primaryBlue"
              :style="{ height: '50px' }"
              rounded
              elevation="12"
              :loading="loading"
              type="submit"
            >
              Send Email
            </v-btn>
            <ErrorCorrectionRequest v-if="emailFormSubmissionAttempted && !emailFormValid" />
          </v-form>
        </v-card-text>
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.button-custom {
  height: 50px;
}

.back-button {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
}

strong {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 19px;
  font-family: poppins;
  margin-bottom: 0px;
  align-items: center;
}

p {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 18px;
  font-family: poppins;
  margin-bottom: 10px;
  font-weight: bold;
}

footer {
  text-align: center;
  font-family: poppins;
  font-weight: bold;
}

.back-button:hover,
.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.back-button .v-icon,
.close-button .v-icon {
  font-size: 20px;
}

.subtitle {
  font-weight: bold;
  opacity: 1;
  font-size: 16px;
}

a {
  text-decoration: underline;
  font-family: 'Poppins';
  font-weight: bold;
}

.logo {
  height: 100px;
}
</style>
