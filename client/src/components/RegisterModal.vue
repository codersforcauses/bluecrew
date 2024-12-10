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

defineEmits(['close'])
</script>

<template>
  <div class="register-container">
    <div class="header">
      <button class="close-button" @click="$emit('close'), $router.push('/')">X</button>
      <img src="/bc-logo.png" alt="logo" style="margin: 0 auto" />
    </div>
    <strong class="text-primaryPink">Create an account</strong>
    <form class="register-form">
      <v-responsive max-width="1200">
        <label for="username" class="text-primaryPink">Username</label>
        <v-text-field
          hide-details="auto"
          label="Enter your username"
          v-model="formData.username"
          class="bg-primaryBrown"
          variant="outlined"
        ></v-text-field>
      </v-responsive>

      <v-responsive max-width="1200">
        <label for="email" class="text-primaryPink">Email</label>
        <v-text-field
          hide-details="auto"
          label="Enter your email"
          v-model="formData.email"
          class="bg-primaryBrown"
          variant="outlined"
        ></v-text-field>
      </v-responsive>

      <v-responsive max-width="1200">
        <label for="firstName" class="text-primaryPink">First Name</label>
        <v-text-field
          hide-details="auto"
          label="Enter your first name"
          v-model="formData.firstName"
          class="bg-primaryBrown"
          variant="outlined"
        ></v-text-field>
      </v-responsive>

      <v-responsive max-width="1200">
        <label for="lastName" class="text-primaryPink">Username</label>
        <v-text-field
          hide-details="auto"
          label="Enter your last name"
          v-model="formData.lastName"
          class="bg-primaryBrown"
          variant="outlined"
        ></v-text-field>
      </v-responsive>

      <div class="form-group">
        <label for="dateOfBirth" class="text-primaryPink">Date of Birth</label>
        <v-date-input
          v-model="formData.dateOfBirth"
          label="Select a date"
          max-width="1200"
        ></v-date-input>
      </div>

      <div class="form-group">
        <label for="genderId" class="text-primaryPink">Gender Identity</label>
        <v-select
          class="bg-primaryBrown"
          label="Select gender identity"
          :items="['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']"
          hide-details
        ></v-select>
      </div>

      <div class="form-group">
        <label for="indigenousTIS" class="text-primaryPink">
          Indigenous or Torres Strait Islander
        </label>
        <v-select
          bg-color="primaryBrown"
          label="Please select"
          :items="['Yes', 'No', 'Prefer not to say']"
          variant="solo-filled"
          hide-details
        ></v-select>
      </div>

      <div class="form-group">
        <label for="password" class="text-primaryPink">Password</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          class="bg-primaryBrown"
          placeholder="Enter your password"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword" class="text-primaryPink">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="formData.confirmPassword"
          class="bg-primaryBrown"
          placeholder="Confirm your password"
        />
      </div>
      <button type="submit" class="bg-primaryBlue text-creamyWhite">Sign Up</button>
    </form>

    <footer class="text-primaryPink">
      Already have an account? <a href="#" class="text-primaryPink">Sign In</a>
    </footer>
  </div>
</template>

<style scoped>
.register-container {
  width: 100%;
  padding: 50px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.register-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 3px;
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
}

a {
  font-weight: bold;
  text-decoration: underline;
}
</style>
