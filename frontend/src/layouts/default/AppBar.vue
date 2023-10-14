<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <a href="/">
      <v-icon>mdi-circle-slice-4</v-icon>
      Anymal
        </a>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <!-- Logout Button -->
    <v-btn v-if="auth.user" icon @click="logout">
      <v-icon>mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import router from "@/router";
import {useAuthStore} from "@/store/auth";
const auth = useAuthStore();
const logout = () => {
  router.push({ name: 'Logout' }); // navigate to logout route
};
</script>
