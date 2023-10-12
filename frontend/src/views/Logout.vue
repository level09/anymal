<template>
  <div>
    Logging out...
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api'; // ensure path to API module is correct

const router = useRouter();

onMounted(async () => {
  try {
    await api.post('/auth/jwt/logout');
    console.log('Logged out successfully');
  } catch (error) {
    console.error('Error during logout:', error);
    // Handle error, e.g., through user notification or additional logging
  } finally {
    // Redirect to home regardless of logout success
    router.push({ name: 'Home' });
  }
});
</script>
