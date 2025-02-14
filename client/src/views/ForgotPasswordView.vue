<template>
  <div class="reset-password">
    <h2>Reset Password</h2>
    <p>Enter your new password below.</p>

    <div class="input-group">
      <label for="password">New Password</label>
      <input id="password" v-model="password" type="password" placeholder="Enter new password" required />
    </div>

    <div class="input-group">
      <label for="confirmPassword">Confirm Password</label>
      <input id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Confirm new password" required />
    </div>

    <button @click="resetPassword">Reset Password</button>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import axios from 'axios';

const props = defineProps<{ token?: string }>(); // receive token as a prop

const password = ref('');
const confirmPassword = ref('');
const message = ref('');

const resetPassword = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = "Passwords do not match.";
    return;
  }

  try {
    await axios.post('/api/reset-password', {
      token: props.token, // using the prop instead of useRoute
      password: password.value,
    });
    message.value = "Password reset successfully!";
  } catch (error) {
    console.error('Password reset failed:', error);
    message.value = "Failed to reset password.";
  }
};
</script>


<style scoped>
.reset-password {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.input-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.message {
  margin-top: 10px;
  font-weight: bold;
}
</style>
