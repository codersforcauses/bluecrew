<script setup lang="ts">
import { reactive } from 'vue'

const formData = reactive({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
})
</script>

<template>
  <div class="register-container">
    <div class="header">
      <button class="close-button" @click="handleClose">×</button>
      <img src="/bc-logo.png"></img>
    </div>
    <strong class="text-primaryPink">Create an account</strong>
    <form class="register-form">
      <div class="form-group">
        <label for="username" class="text-primaryPink">Username</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          class = "bg-primaryBrown"
          placeholder="Enter your username"
        />
      </div>

      <div class="form-group">
        <label for="email" class="text-primaryPink">Email</label>
        <input 
        type="email" 
        id="email" 
        v-model="formData.email" 
        class = "bg-primaryBrown"
        placeholder="Enter your email" />
      </div>

      <div class="form-group">
        <label for="firstName" class="text-primaryPink">First Name</label>
        <input
          type="firstName"
          id="firstName"
          v-model="formData.firstName"
          class = "bg-primaryBrown"
          placeholder="Enter your first name"
        />
      </div>

      <div class="form-group">
        <label for="lastName" class="text-primaryPink">Last Name</label>
        <input
          type="lastName"
          id="lastName"
          v-model="formData.lastName"
          class = "bg-primaryBrown"
          placeholder="Enter your last name"
        />
      </div>

      <div class="form-group">
        <label for="password" class="text-primaryPink">Password</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          class = "bg-primaryBrown"
          placeholder="Enter your password"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword" class="text-primaryPink">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="formData.confirmPassword"
          class = "bg-primaryBrown"
          placeholder="Confirm your password"
        />
      </div>
      <button type="submit" class="bg-primaryBlue text-creamyWhite" :disabled="!isFormValid">Sign Up</button>
    </form>

    <footer class="text-primaryPink">Already have an account?  Sign In</footer>
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

.close-button {
  display: flex;
  justify-content: flex-end;
  font-size: 24px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px 10px;
  box-shadow: none;
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
  margin-bottom: 10px; /* 每个表单组之间的间距 */
}

strong {
  width: 100%;
  display: flex;
  flex-direction: column;
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

footer {
  font-weight: bold;
}

</style>
