import {createRouter, createWebHistory} from 'vue-router';
import {useAuthStore} from "@/store/auth";

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {path: '', name: 'Home', component: () => import('@/views/Home.vue'), meta: {requiresAuth: false}},
      {path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta: {requiresAuth: true}},
      {path: 'register', name: 'Register', component: () => import('@/views/Register.vue'), meta: {requiresAuth: false}},
      {path: 'logout', name: 'Logout', component: () => import('@/views/Logout.vue'), meta: {requiresAuth: true}},
      {path: 'login', name: 'Login', component: () => import('@/views/Login.vue'), meta: {requiresAuth: false}},
      {path: 'auth/google/callback', name: 'googleAuthCallback', component: () => import('@/views/AuthCallback.vue'), meta: {requiresAuth: false}},
      {path: 'success', name: 'Success', component: () => import('@/views/Success.vue'), meta: {requiresAuth: true}},
      {path: 'cancelled', name: 'Cancelled', component: () => import('@/views/Cancelled.vue'), meta: {requiresAuth: true}},
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  if (!auth.isAuthenticated) {
    await auth.checkAuthentication();
  }

  console.log('Routing from', from.fullPath, 'to', to.fullPath, 'isAuthenticated:', auth.isAuthenticated);

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    console.log('Unauthenticated user navigating to protected route - redirecting to Login');
    next({name: 'Login'});
  } else if (!to.meta.requiresAuth) {
    // If user is authenticated and tries to visit a public page (like Login), redirect to Dashboard.
    if (auth.isAuthenticated && to.name === 'Login') {
      console.log('Authenticated user navigating to Login - redirecting to Dashboard');
      next({name: 'Dashboard'});
    } else {
      console.log('Public route - allowing navigation');
      next();
    }
  } else {
    console.log('Allowing navigation');
    next();
  }
});


export default router;
