<template>
  <div>
    Authenticating...
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const error = ref(null);

onMounted(async () => {
  const code = route.query.code;

  try {
    // Send the code to the backend, get user/token in return
    const response = await axios.post('http://localhost:8000/auth/google/callback', { code });
    // Handle the response accordingly, e.g., store the token, etc.

    localStorage.setItem('accessToken', response.data.access_token);

    // Redirect to the dashboard or desired page
    router.push({ name: 'Dashboard' });
  } catch (err) {
    error.value = "Authentication failed!";
    console.error('Error:', err);
    // Optionally handle the error, e.g., redirect to login with a flash message, etc.
  }
});
</script>

<style>
/* Add any necessary styling */
</style>
