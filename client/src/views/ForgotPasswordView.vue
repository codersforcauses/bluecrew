<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { useMessageStore } from '@/stores/message'
import axios from 'axios';

const props = defineProps<{ token?: string }>(); // receive token as a prop
const messageStore = useMessageStore()
const password = ref('');
const confirmPassword = ref('');

const resetPassword = async () => {
  if (password.value !== confirmPassword.value) {
    messageStore.showMessage('Error', 'Passwords do not match.', 'error');
    return;
  }

  try {
    await axios.post('/api/reset-password', {
      token: props.token, // using the prop instead of useRoute
      password: password.value,
    });
   messageStore.showMessage('Success', 'Password has been reset', 'success');
  } catch (error) {
    console.error('Password reset failed:', error);
    messageStore.showMessage('Error', 'Failed to reset password. Please try again.', 'error');
  }
};
</script>
<template>
  <div class="reset-password-container">
    <div class="reset-password">
      <h2 class="text-primaryGreen">Reset Password</h2>
      <p class="text-primaryGreen">Enter your new password below.</p>

      <div class="input-group">
        <label class="text-primaryGreen" for="password">New Password</label>
        <v-text-field class="mt-2" bg-color="primaryBrown" id="password" v-model="password" type="password" placeholder="Enter new password" required />
      </div>

      <div class="input-group">
        <label class="text-primaryGreen" for="confirmPassword">Confirm Password</label>
        <v-text-field class="mt-2" bg-color="primaryBrown" id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Confirm new password" required />
      </div>
      
      <v-btn class="d-flex justify-center mt-8 w-50 mx-auto" color="primaryBlue" height="50px" font-family="Lilita One, cursive" rounded @click="resetPassword">Reset Password</v-btn>

    </div>
  </div>
</template>



<style scoped>
.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
  overflow: hidden;
}

h2 {
  font-family: "Lilita One", cursive;
  font-size: 40px
}

p {
  font-family: "Poppins";
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
  margin-bottom: 20px; /* Adjust the spacing as needed */
}

.input-group {
  text-align: left;
  font-family: "Poppins";
  font-size: 18px;
  font-weight: bold;
}

.message {
  font-family: "Poppins";
  font-size: 18px;
  font-weight: bold;
  color: red;
}
</style>
