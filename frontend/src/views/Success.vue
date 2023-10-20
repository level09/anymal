<template>
   <v-container class="text-center" fluid>
     <v-card>
       <v-card-title>Success</v-card-title>
       <v-card-text>
         Subscription to Starter plan successful!
       </v-card-text>
     </v-card>

  </v-container>
  <section>
    <div class="product">
      <!-- SVG content here (for brevity, I'm not including the SVG content in this example) -->
      <div class="description">

      </div>
    </div>
    <v-btn @click="manageBilling">Manage your billing information</v-btn>
  </section>
</template>

<script>
import api from "@/plugins/api";

export default {
  data() {
    return {
      sessionId: null  // You can get this from the route/query if needed
    };
  },
  methods: {
    async manageBilling() {
      try {
        const response = await api.post('/create-portal-session', { session_id: this.sessionId });
        if (response.status === 200) {
          window.location.href = response.data.portal_url;  // Assuming the API returns a portal_url to redirect to
        }
      } catch (error) {
        console.error('Error navigating to billing portal:', error);
      }
    }
  },
  mounted() {
    // Assuming you're passing the session ID as a query parameter named 'session_id'
    this.sessionId = this.$route.query.session_id;
  }
};
</script>
