<script setup>
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
    <h3>Create an account</h3>
    <form class="register-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="formData.username" />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="formData.email" />
      </div>

      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="firstName" id="firstName" v-model="formData.firstName" />
      </div>

      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input type="lastName" id="lastName" v-model="formData.lastName" />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="formData.password" />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="formData.confirmPassword" />
      </div>
      <button type="submit" :disabled="!isFormValid">Sign Up</button>
    </form>

    <h3>Already have an account?Sign In</h3>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: bold;
  color: #555;
}

input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.2);
}

.error-message {
  color: #f44336;
  font-size: 14px;
}

button {
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
