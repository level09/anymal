<template>
  <div>
    Logging out...
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/store/auth";
import api from "@/plugins/api";

const router = useRouter();
const auth = useAuthStore();

onMounted(async () => {
  try {
    await api.post('/auth/jwt/logout');
    console.log('Logged out successfully');
  } catch (error) {
    console.error('Error during logout:', error);
  } finally {
    // Update the local state to reflect that the user is logged out.
    auth.setAuthenticated(false);
    // Redirect to home regardless of logout success
    router.push({ name: 'Home' });
  }
});
</script>
