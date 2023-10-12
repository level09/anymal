<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height">
      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <v-card variant="elevated" class="pa-4" width="550" color="">
            <v-card-title class="my-3">Login</v-card-title>

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
              <v-btn width="100" elevated @click="login" :loading="loading" color="primary" class="mb-4"
                     variant="elevated">Login
              </v-btn>


              <v-btn @click="loginWithGoogle" variant="elevated" class="mb-4">

                <template v-slot:prepend>
                  <v-img
                    src="https://developers.google.com/identity/images/g-logo.png"
                    contain
                    height="24"
                    width="24"
                    class="me-2"
                  ></v-img>
                  Sign in with Google
                </template>


              </v-btn>

            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import {ref} from 'vue';
import router from "@/router";
import api from "@/api";


const email = ref('');
const password = ref('');
const loading = ref(false);
window.router = router;
const login = async () => {
  loading.value = true;
  try {
    await api.post(
      '/auth/jwt/login',

      {
        username: email.value,
        password: password.value
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    console.log('Login successful');
    router.push('/dashboard');
  } catch (error) {
    console.error('Login failed:', error);
  } finally {
    loading.value = false;
  }
};

const loginWithGoogle = async () => {
  loading.value = true;
  try {
    const response = await api.get('/auth/google/authorize');
    window.location.href = response.data.authorization_url;
  } catch (error) {
    console.error('Google login initiation failed:', error);
  } finally {
    loading.value = false;
  }
};
</script>
