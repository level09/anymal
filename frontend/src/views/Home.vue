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
            <v-btn large class="mx-3" href="/login">Login</v-btn>
            <v-btn large class="mx-3" href="/signup" color="primary">Sign Up</v-btn>
            <v-btn large class="mx-3" href="/dashboard" color="orange">Dashbaord</v-btn>
          </v-col>
        </v-row>
      </v-container>



      <!-- Footer -->
      <v-footer color="indigo" class="white--text mt-16" >
        <v-col class="text-center" sm="4">
          <span>2023 &copy; Awesome Saas</span>
        </v-col>
        <v-col class="text-center" sm="4">
          <span>Connect with Us</span>
        </v-col>
        <v-col class="text-center" sm="4">
          <span>Contact</span>
        </v-col>
      </v-footer>
    </v-main>
  </v-app>
</template>

<script>
export default {
  // No data() function since all values are hardcoded in the markup
}
</script>

