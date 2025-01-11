<script setup lang="ts">
import { ref, computed } from 'vue'
import { useModalStore } from '@/stores/modal'
import type { UserRegistrationForm } from '@/types/user'
import { useDisplay } from 'vuetify'

const { xs } = useDisplay()
const modalStore = useModalStore()

const formData = ref<UserRegistrationForm>({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  dateOfBirth: '',
  genderId: null,
  indigenousTIS: null,
  password: '',
  confirmPassword: '',
})

const isDialogVisible = computed({
  get: () => modalStore.currentModal === 'register',
  set: (value: boolean) => {
    if (!value) {
      modalStore.closeModal()
    }
  },
})

const closeDialog = () => {
  modalStore.closeModal()
}

const submitForm = async () => {
  // Copies formData but creates first_name and last_name in snake case for variable compatability
  const body = {
    ...formData.value,
    first_name: formData.value.firstName,
    last_name: formData.value.lastName,
  }
  try {
    // API call to register
    const response = await fetch('http://localhost:8000/api/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (response.ok) {
      const data = await response.json()
      console.log('Registration successful:', data)
      alert('Registration successful!')
      closeDialog()
    } else {
      const errorData = await response.json()
      console.error('Registration failed:', errorData)
      alert(`Error: ${errorData.message || 'Registration failed.'}`)
    }
  } catch (error) {
    console.error('Network error:', error)
    alert('Network error. Please try again.')
  }
}
</script>

<template>
  <div>
    <v-dialog
      v-model="isDialogVisible"
      :max-width="xs ? '100%' : '400px'"
      :fullscreen="xs"
      scrollable
      persistent
    >
      <v-card>
        <v-card-text style="height: auto; overflow-y: auto">
          <div class="header">
            <button class="close-button" @click="closeDialog">x</button>
            <img src="/bc-logo.png" alt="logo" style="margin: 0 auto" />
          </div>
          <strong class="text-primaryPink">Create an account</strong>
          <form class="register-form" @submit.prevent="submitForm">
            <div class="form-group">
              <label for="username" class="text-primaryPink">Username</label>
              <v-text-field
                hide-details="auto"
                placeholder="Enter your username"
                v-model="formData.username"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="email" class="text-primaryPink">Email</label>
              <v-text-field
                hide-details="auto"
                placeholder="Enter your email"
                v-model="formData.email"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="firstName" class="text-primaryPink">First Name</label>
              <v-text-field
                hide-details="auto"
                placeholder="Enter your first name"
                v-model="formData.firstName"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="lastName" class="text-primaryPink">Last Name</label>
              <v-text-field
                hide-details="auto"
                placeholder="Enter your last name"
                v-model="formData.lastName"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="dateOfBirth" class="text-primaryPink">Date of Birth</label>
              <v-text-field
                type="date"
                hide-details="auto"
                placeholder="dd-mm-yyyy"
                v-model="formData.dateOfBirth"
                class="bg-primaryBrown"
                variant="outlined"
                persistent-placeholder
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="genderId" class="text-primaryPink">Gender Identity</label>
              <v-select
                hide-details="auto"
                class="bg-primaryBrown"
                placeholder="Select your gender identity"
                :items="['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']"
                v-model="formData.genderId"
                variant="outlined"
              ></v-select>
            </div>

            <div class="form-group">
              <label for="indigenousTIS" class="text-primaryPink">
                Indigenous or Torres Strait Islander
              </label>
              <v-select
                hide-details="auto"
                class="bg-primaryBrown"
                placeholder="Please select"
                :items="['Yes', 'No', 'Prefer not to say']"
                v-model="formData.indigenousTIS"
                variant="outlined"
              ></v-select>
            </div>

            <div class="form-group">
              <label for="password" class="text-primaryPink">Password</label>
              <v-text-field
                hide-details="auto"
                placeholder="Enter your password"
                v-model="formData.password"
                type="password"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="text-primaryPink">Confirm Password</label>
              <v-text-field
                hide-details="auto"
                placeholder="Confirm your password"
                v-model="formData.confirmPassword"
                type="password"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>
            <v-btn
              id="register-button"
              class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center"
              @click="submitForm"
              >Sign Up</v-btn
            >
          </form>

          <footer class="text-primaryPink">
            Already have an account? <a href="#" class="text-primaryPink">Sign In</a>
          </footer>
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
  font-size: 20px;
  font-family: poppins;
  margin-bottom: 10px;
  align-items: center;
  font-weight: bold;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 10px;
  width: 100px;
}

label {
  font-weight: bold;
  font-family: poppins;
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.16);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.close-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-self: flex-end;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  background: none;
  color: black;
  border: 3px;
  border-color: black;
  cursor: pointer;
  padding: 0;
}

footer {
  text-align: center;
  font-family: poppins;
  font-weight: bold;
}

a {
  text-decoration: underline;
  font-family: poppins;
  font-weight: bold;
}
</style>
