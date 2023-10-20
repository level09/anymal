<template>
  <v-app>
    <v-main>
      <!-- Header Section -->
      <v-container class="text-center" fluid>
        <v-row>
          <v-col>
            <h1 class="display-1">Awesome Saas</h1>
            <p class="subtitle-1">Centralized Management for your Business</p>
          </v-col>
        </v-row>
      </v-container>

      <!-- Call to Action -->
      <v-container class="text-center" fluid>
        <v-row>
          <v-col>
            <v-btn v-if="!auth.user" large class="mx-3" href="/login">Login</v-btn>
            <v-btn v-if="!auth.user" large class="mx-3" href="/register" color="primary">Sign Up</v-btn>
            <v-btn large class="mx-3" href="/dashboard" color="orange">Dashboard</v-btn>


          </v-col>
        </v-row>
      </v-container>

      <!-- Footer -->
      <v-footer color="indigo" class="white--text mt-16">
        <v-col class="text-center" sm="3">
          <span>2023 &copy; Awesome Saas</span>
        </v-col>
        <v-col class="text-center" sm="3">
          <span>Connect with Us</span>
        </v-col>
        <v-col class="text-center" sm="3">
          <span>Contact</span>
        </v-col>
        <v-col class="text-center" sm="3">
          <span></span>
        </v-col>
      </v-footer>
    </v-main>
  </v-app>
</template>

<script>
import { useAuthStore } from "@/store/auth";
import api from "@/plugins/api";

export default {
  data() {
    return {
      auth: useAuthStore()
    };
  },
  methods: {

  }
};
</script>

