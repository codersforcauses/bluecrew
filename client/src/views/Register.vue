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
    <div class="header">
      <button class="close-button" @click="handleClose">×</button>
    </div>
    <p class="form-header">Create an account</p>
    <form class="register-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          placeholder="Enter your username"
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="formData.email" placeholder="Enter your email" />
      </div>

      <div class="form-group">
        <label for="firstName">First Name</label>
        <input
          type="firstName"
          id="firstName"
          v-model="formData.firstName"
          placeholder="Enter your first name"
        />
      </div>

      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input
          type="lastName"
          id="lastName"
          v-model="formData.lastName"
          placeholder="Enter your last name"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          placeholder="Enter your password"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="formData.confirmPassword"
          placeholder="Confirm your password"
        />
      </div>
      <button type="submit" :disabled="!isFormValid">Sign Up</button>
    </form>

    <footer>Already have an account?Sign In</footer>
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
}
.form-header {
  width: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  align-items: center;
  font-weight: bold;
  color: red;
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
label {
  font-weight: bold;
  color: red;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  background: burlywood;
}
button {
  width: 100%;
  padding: 12px;
  background-color: #28365f;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}
footer {
  color: red;
}
</style>
