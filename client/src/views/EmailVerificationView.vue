<template>
    <div class="d-flex justify-center align-center full-screen">
    <h2>Verifying your email...</h2>
  </div>
</template>

<style scoped>
.full-screen {
  height: 100vh;
}
</style>

<script setup lang="ts">
import { onMounted } from 'vue';
import axios from 'axios';

// use defineProps to receive the token from the router
const props = defineProps<{ token?: string }>();

onMounted(async () => {
  if (!props.token) {
    alert('Invalid verification link.');
    return;
  }

  try {
    await axios.post('/api/verify-email', {
      token: props.token,
    });
    alert('Email verified successfully');
  } catch (error) {
    console.error('Email verification failed:', error);
    alert('Email verification failed');
  }
});

</script>
