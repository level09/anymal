import { defineStore } from 'pinia';
import api from "@/plugins/api";

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    isAuthenticated: false,
  }),
  actions: {
    setAuthenticated(authenticated) {
      this.isAuthenticated = authenticated;
    },
    async checkAuthentication() {
      try {
        const response = await api.get('/users/me');
        if(response.data) {
          // If successful, 'response.data' will contain user details.
          this.setAuthenticated(true);
        } else {
          this.setAuthenticated(false);
        }
      } catch (error) {
        console.error("Error checking authentication status:", error);
        this.setAuthenticated(false);
      }
    },
  },
});
