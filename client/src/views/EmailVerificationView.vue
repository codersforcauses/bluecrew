<template>
  <div>
    <h2>Verifying your email...</h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';


// use defineProps to receive the token from the router
const props = defineProps<{ token?: string }>();

/* REAL IMPLEMENTATION
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
*/

// SIMULATION ONLY == DELETED SOON ==
// by typing: http://localhost:3000/verify-email?token=test
onMounted(() => {
  console.log('Token from props:', props.token);

  // Simulate successful email verification without backend
  if (!props.token) {
    alert('Invalid verification link. Simulating failure.');
    return;
  }

  // Simulate success scenario directly
  console.log('[SIMULATION] Email verified successfully with token:', props.token);
  alert('Email verified successfully (simulated).');
});

</script>
