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
    <v-btn icon @click="logout">
      <v-icon>mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
import router from "@/router";
const logout = () => {
  router.push({ name: 'Logout' }); // navigate to logout route
};
</script>
