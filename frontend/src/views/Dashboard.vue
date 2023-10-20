<template>
  <v-container class="text-center" fluid="">
    <v-card>
      <v-card-title>Dashboard</v-card-title>
      <!-- Stripe Subscription Buttons -->
      <v-btn large class="mx-3" color="green" @click="startCheckout">Start Subscription</v-btn>
      <v-btn large class="mx-3" color="blue" @click="goToCustomerPortal">Customer Portal</v-btn>
      <v-card-text>Welcome, {{ auth.user.email }}</v-card-text>
    </v-card>
  </v-container>


</template>

<script>
import {useAuthStore} from "@/store/auth";
import api from "@/plugins/api";

export default {
  data() {
    return {
      auth: useAuthStore()
    }


  },

  mounted() {


  },

  methods: {
    async startCheckout() {
      try {
        const lookupKey = import.meta.env.VITE_PRODUCT_LOOKUP_KEY;  // Replace with the appropriate lookup key

        const response = await api.post(`/stripe/create-checkout-session?lookup_key=${lookupKey}`);

        if (response.status !== 200) {
          throw new Error('Failed to create checkout session');
        }

        // Redirect the user to the Stripe checkout page
        window.location.href = response.data.checkout_url;
      } catch (error) {
        console.error('Error starting checkout:', error);
      }
    },

    async goToCustomerPortal() {
      try {
        const response = await api.post('/stripe/create-portal-session');

        if (response.status !== 200) {
          throw new Error('Failed to create portal session');
        }

        // Redirect the user to the Stripe customer portal using the received URL
        window.location.href = response.data.portal_url;
      } catch (error) {
        console.error('Error accessing customer portal:', error);
      }
    }

  }
}
</script>
