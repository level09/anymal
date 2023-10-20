<template>
  <div>
    Authenticating ...
  </div>
</template>

<script>
import api from "@/plugins/api";

export default {
  name: 'AuthCallback',
  mounted() {
    // Forward the current route's query parameters directly to the Axios request
    api.get('/auth/google/callback', {
      params: this.$route.query
    })
      .then(response => {
        // Redirect to the dashboard route
        this.$router.push('/dashboard');
      })
      .catch(err => {
        // Handle the error if needed
        console.error('Error during authentication:', err);
        // Optionally, you can redirect to an error page or show an error message
      });
  }
}
</script>
