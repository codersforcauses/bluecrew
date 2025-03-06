<script setup lang="ts">
import { ref, computed } from 'vue'
import { useModalStore } from '@/stores/modal'
import type { BackendUser, UserRegistrationForm, UserRegistrationFormFields } from '@/types/user'
import { useDisplay } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useMessageStore } from '@/stores/message'
import ErrorCorrectionRequest from './ErrorCorrectionRequest.vue'

const { xs } = useDisplay()
const modalStore = useModalStore()
const userStore = useUserStore()
const messageStore = useMessageStore()

const currentPage = ref<'register' | 'confirmation'>('register')

const indigenousIdentites = ['Prefer not to say', 'Yes', 'No']
const genderIdentities = ['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']

const formData = ref<UserRegistrationForm>({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  dateOfBirth: '',
  genderId: genderIdentities[4],
  indigenousTIS: indigenousIdentites[0],
  password: '',
  confirmPassword: '',
})

const formServerErrors = ref<UserRegistrationForm>({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  dateOfBirth: '',
  genderId: '',
  indigenousTIS: '',
  password: '',
  confirmPassword: '',
})

const formFields: UserRegistrationFormFields[] = [
  {
    formAttribute: 'username',
    fieldName: 'Username',
    fieldPlaceholder: 'Enter your username',
    fieldType: 'text',
  },
  {
    formAttribute: 'email',
    fieldName: 'Email',
    fieldPlaceholder: 'Enter your email',
    fieldType: 'email',
  },
  {
    formAttribute: 'firstName',
    fieldName: 'First Name',
    fieldPlaceholder: 'Enter your first name',
    fieldType: 'text',
  },
  {
    formAttribute: 'lastName',
    fieldName: 'Last Name',
    fieldPlaceholder: 'Enter your last name',
    fieldType: 'text',
  },
  {
    formAttribute: 'dateOfBirth',
    fieldName: 'Date of Birth',
    fieldPlaceholder: 'dd-mm-yyyy',
    fieldType: 'date',
  },
  {
    formAttribute: 'genderId',
    fieldName: 'Gender Identity',
    fieldPlaceholder: 'Select your gender identity',
    fieldType: 'text',
    dropDownItems: genderIdentities,
  },
  {
    formAttribute: 'indigenousTIS',
    fieldName: 'Indigenous or Torres Strait Islander',
    fieldPlaceholder: 'Please select',
    fieldType: 'text',
    dropDownItems: indigenousIdentites,
  },
  {
    formAttribute: 'password',
    fieldName: 'Password',
    fieldPlaceholder: 'Enter your password',
    fieldType: 'password',
  },
  {
    formAttribute: 'confirmPassword',
    fieldName: 'Confirm Password',
    fieldPlaceholder: 'Confirm your password',
    fieldType: 'password',
  },
]

const valid = ref(false)
const loading = ref(false)
const formSubmissionAttempted = ref(false)
const required = (value: string) => !!value || 'Required.'
const emailProbablyValid = (value: string) => /^\S+@\S+\.\S+$/.test(value) || 'Invalid e-mail.'
const passwordsMatch = (value: string) =>
  value === formData.value.password || 'Passwords do not match.'

const getRules = (type: 'text' | 'email' | 'password' | 'date') => {
  switch (type) {
    case 'email':
      return [emailProbablyValid, required]
    case 'password':
      return [passwordsMatch, required]
    default:
      return [required]
  }
}

const isDialogVisible = computed({
  get: () => modalStore.currentModal === 'register',
  set: (value: boolean) => {
    if (!value) {
      modalStore.closeModal()
    }
  },
})

const setCurrentPage = (page: 'register' | 'confirmation') => {
  currentPage.value = page
}

const submitForm = async () => {
  formSubmissionAttempted.value = true
  if (!valid.value) {
    return
  }
  loading.value = true
  const body: BackendUser = {
    username: formData.value.username,
    email: formData.value.email,
    first_name: formData.value.firstName,
    last_name: formData.value.lastName,
    birthdate: formData.value.dateOfBirth,
    gender_identity: genderIdentities.indexOf(formData.value.genderId),
    indigenous_identity: indigenousIdentites.indexOf(formData.value.indigenousTIS),
    password: formData.value.password,
  }
  const registrationResult = await userStore.registerUser(body)
  if (registrationResult === true) {
    const verificationResult = await userStore.requestEmailVerification(formData.value.email)
    if (verificationResult === true) {
      setCurrentPage('confirmation')
    } else if (verificationResult === false) {
      messageStore.handleUnexpectedError(undefined, false)
    } else {
      messageStore.showMessage('Error', verificationResult, 'warning')
    }
  } else if (registrationResult === false) {
    messageStore.handleUnexpectedError(undefined, true)
  } else {
    const nameMapping: Array<{
      serverName: keyof BackendUser
      clientName: keyof UserRegistrationForm
    }> = [
      { serverName: 'username', clientName: 'username' },
      { serverName: 'first_name', clientName: 'firstName' },
      { serverName: 'last_name', clientName: 'lastName' },
      { serverName: 'email', clientName: 'email' },
      { serverName: 'birthdate', clientName: 'dateOfBirth' },
      { serverName: 'password', clientName: 'password' },
    ]
    nameMapping.forEach(({ serverName, clientName }) => {
      if (registrationResult[serverName]) {
        const errorFromServer = registrationResult[serverName][0]
        // make sure the error from the server is capitalized correctly
        formServerErrors.value[clientName] = errorFromServer
          ? errorFromServer[0].toUpperCase() + errorFromServer.slice(1)
          : ''
      }
    })
  }
  loading.value = false
}

const closeDialog = () => {
  modalStore.closeModal()
}

const openLoginModal = () => {
  modalStore.openLogin()
}
</script>

<template>
  <div>
    <v-dialog
      v-model="isDialogVisible"
      :max-width="xs ? '100%' : '500px'"
      :fullscreen="xs"
      scrollable
      persistent
    >
      <v-card>
        <v-card-text style="height: auto; overflow-y: auto">
          <template v-if="currentPage === 'register'">
            <div class="header">
              <button class="close-button" @click="closeDialog">
                <v-icon icon="mdi-close-circle-outline" />
              </button>
              <img src="/blingo-logo.svg" alt="logo" class="logo" />
            </div>

            <strong class="text-primaryGreen">Create an account</strong>

            <v-form
              v-model="valid"
              class="register-form"
              @submit.prevent="submitForm"
              validate-on="invalid-input"
            >
              <div v-for="(formField, index) in formFields" class="form-group" :key="index">
                <label :for="`register-${formField.formAttribute}`" class="text-primaryGreen">{{
                  formField.fieldName
                }}</label>
                <v-select
                  v-if="formField.dropDownItems"
                  :id="`register-${formField.formAttribute}`"
                  hide-details="auto"
                  :placeholder="formField.fieldPlaceholder"
                  v-model="formData[formField.formAttribute]"
                  bg-color="primaryBrown"
                  variant="outlined"
                  :items="formField.dropDownItems"
                />
                <v-text-field
                  v-else
                  :id="`register-${formField.formAttribute}`"
                  hide-details="auto"
                  :placeholder="formField.fieldPlaceholder"
                  v-model="formData[formField.formAttribute]"
                  bg-color="primaryBrown"
                  variant="outlined"
                  :type="formField.fieldType"
                  :rules="getRules(formField.fieldType)"
                  :error-messages="formServerErrors[formField.formAttribute]"
                  @focus="formServerErrors[formField.formAttribute] = ''"
                />
              </div>
              <v-btn
                class="d-flex justify-center mt-4 w-50 mx-auto"
                color="primaryBlue"
                :style="{ height: '50px' }"
                rounded
                :loading="loading"
                elevation="12"
                type="submit"
              >
                Sign Up
              </v-btn>
              <ErrorCorrectionRequest v-if="formSubmissionAttempted && !valid" />
            </v-form>

            <footer class="text-primaryGreen">
              Already have an account?
              <a class="text-primaryGreen cursor-pointer" @click.prevent="openLoginModal"
                >Sign In</a
              >
            </footer>
          </template>

          <template v-if="currentPage === 'confirmation'">
            <div class="header">
              <button class="close-button" @click="closeDialog">
                <v-icon icon="mdi-close-circle-outline" />
              </button>
              <img src="/blingo-logo.svg" alt="Blingo Logo" class="logo" />
            </div>
            <h2 class="text-primaryGreen text-center">One More Step</h2>
            <p class="text-center">Please check your inbox for a link to verify your email.</p>
            <v-btn
              class="d-flex justify-center mt-4 w-50 mx-auto"
              color="primaryBlue"
              :style="{ height: '50px' }"
              rounded
              elevation="12"
              @click="closeDialog"
            >
              Close
            </v-btn>
          </template>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.register-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

strong {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-size: 25px;
  font-family: 'Lilita One', cursive;
  margin-bottom: 10px;
  align-items: center;
  font-weight: bold;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 10px;
  margin-top: -30px;
  width: 100px;
}

label {
  font-weight: bold;
  font-family: 'Poppins';
  padding-bottom: 10px;
}

button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-family: poppins;
  font-size: 16px;
  margin-top: 10px;
  margin-right: 10px;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.close-button {
  width: 40px;
  height: 40px;
  margin-right: 0px;
  display: flex;
  align-self: flex-end;
  justify-content: center;
  align-items: center;
  font-size: 21px;
  cursor: pointer;
  padding: 0;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.close-button .v-icon {
  font-size: 20px;
  margin-top: 0;
}

footer {
  text-align: center;
  font-family: 'Poppins';
  font-weight: bold;
}

a {
  text-decoration: underline;
  font-family: 'Poppins';
  font-weight: bold;
}

.logo {
  height: 100px;
  width: 100%;
}

h2,
p {
  font-family: 'Poppins';
}
</style>
