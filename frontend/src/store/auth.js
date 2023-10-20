import {defineStore} from 'pinia';
import api from "@/plugins/api";

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    isAuthenticated: false,
    user: null, // To store user data
  }),
  actions: {
    // Action to set user data
    setUser(user) {
      this.user = user;
    },
    // Action to set authentication status
    setAuthenticated(authenticated) {
      this.isAuthenticated = authenticated;
    },
    // Action to check authentication status and set user data
    async checkAuthentication() {
      try {
        const response = await api.get('/users/me');
        if (response.data) {
          this.setAuthenticated(true);
          this.setUser(response.data); // Set user data
        } else {
          this.setAuthenticated(false);
          this.setUser(null); // Clear user data if not authenticated
        }
      } catch (error) {
        //console.error("Error checking authentication status:", error);
        this.setAuthenticated(false);
        this.setUser(null); // Clear user data if an error occurs
      }
    },
    // Action to handle logout
    logout() {
      // Clear user data and authentication status
      this.setAuthenticated(false);
      this.setUser(null);
      // Optionally: Redirect to a public page or perform additional cleanup
    },
  },
});
