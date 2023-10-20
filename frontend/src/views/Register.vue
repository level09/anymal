<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <v-card variant="elevated" class="pa-4" width="550" color="">
            <v-card-title class="my-3">Register</v-card-title>

            <v-card-text>
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
              ></v-text-field>
            </v-card-text>
            <v-card-actions class=" px-4">
              <v-btn width="100" elevated @click="register" :loading="loading" color="primary" class="mb-4"
                     variant="elevated">Register
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
import router from "@/router";
import api from "@/plugins/api";

export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false
    };
  },

  methods: {
    async register() {
      this.loading = true;
      try {
        const response = await api.post(
          '/auth/register',
          {
            email: this.email,
            password: this.password,
            is_active: true,
            is_superuser: false,
            is_verified: false
          }
        );

        console.log('Registration successful');
        router.push('/login'); // Redirect to login after successful registration
      } catch (error) {
        console.error('Registration failed:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
