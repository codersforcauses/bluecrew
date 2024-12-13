<script setup lang="ts">
import { ref, defineEmits } from 'vue'

const formData = ref({
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

const dialog = ref(false)
const emit = defineEmits(['close'])
const datePickerDialog = ref(false)

const openDialog = () => {
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  emit('close')
}

const openDatePicker = () => {
  datePickerDialog.value = true
}

const closeDatePicker = () => {
  datePickerDialog.value = false
}

const selectDate = (value: string | null) => {
  if (value) {
    const date = new Date(value)
    formData.value.dateOfBirth = `${String(date.getDate()).padStart(2, '0')}-${String(date.getMonth() + 1).padStart(2, '0')}-${date.getFullYear()}`
    closeDatePicker()
  }
}

const submitForm = () => {
  closeDialog()
}
</script>

<template>
  <div>
    <v-btn id="register-button" class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center" @click="openDialog" text="Registration"></v-btn>
    
    <v-dialog 
      v-model="dialog" 
      max-width="400px" 
      scrollable 
      persistent
    >
      <v-card>
        <v-card-text style="height: auto; overflow-y: auto">
          <div class="header">
            <button class="close-button" @click="closeDialog">X</button>
            <img src="/bc-logo.png" alt="logo" style="margin: 0 auto" />
          </div>
          <strong class="text-primaryPink">Create an account</strong>
          <form class="register-form" @submit.prevent="submitForm">
            <div class="form-group">
              <label for="username" class="text-primaryPink">Username</label>
              <v-text-field
                hide-details="auto"
                label="Enter your username"
                v-model="formData.username"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="email" class="text-primaryPink">Email</label>
              <v-text-field
                hide-details="auto"
                label="Enter your email"
                v-model="formData.email"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="firstName" class="text-primaryPink">First Name</label>
              <v-text-field
                hide-details="auto"
                label="Enter your first name"
                v-model="formData.firstName"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="lastName" class="text-primaryPink">Last Name</label>
              <v-text-field
                hide-details="auto"
                label="Enter your last name"
                v-model="formData.lastName"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>

            <div class="form-group">
              <label for="dateOfBirth" class="text-primaryPink">Date of Birth</label>
              <v-text-field
                hide-details="auto"
                label="Select a date"
                placeholder="dd-mm-yyyy"
                v-model="formData.dateOfBirth"
                class="bg-primaryBrown"
                variant="outlined"
                readonly
                persistent-placeholder
                @click="openDatePicker"
              ></v-text-field>
              
              <v-dialog
                v-model="datePickerDialog"
              >
                <v-card>
                  <v-row justify="space-around">
                    <v-date-picker
                      @update:model-value="selectDate"
                      min-height="300px"
                      min-width="50px"
                      show-adjacent-months
                    ></v-date-picker>
                  </v-row>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center" @click="closeDatePicker">Cancel</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>

            <div class="form-group">
              <label for="genderId" class="text-primaryPink">Gender Identity</label>
              <v-select
                class="bg-primaryBrown"
                label="Select gender identity"
                :items="['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']"
                v-model="formData.genderId"
                hide-details="auto"
                variant="outlined"
              ></v-select>
            </div>

            <div class="form-group">
              <label for="indigenousTIS" class="text-primaryPink">
                Indigenous or Torres Strait Islander
              </label>
              <v-select
                class="bg-primaryBrown"
                label="Please select"
                :items="['Yes', 'No', 'Prefer not to say']"
                v-model="formData.indigenousTIS"
                variant="outlined"
                hide-details
              ></v-select>
            </div>

            <div class="form-group">
              <label for="password" class="text-primaryPink">Password</label>
              <v-text-field
                hide-details="auto"
                label="Enter your password"
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
                label="Confirm your password"
                v-model="formData.confirmPassword"
                type="password"
                class="bg-primaryBrown"
                variant="outlined"
              ></v-text-field>
            </div>
            <v-btn id="register-button" class="bg-primaryBlue text-creamyWhite d-flex justify-center align-center">Sign Up</v-btn>
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
  padding-bottom: 10px;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
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
  font-weight: bold;
  text-align: center;
}

a {
  font-weight: bold;
  text-decoration: underline;
}
</style>