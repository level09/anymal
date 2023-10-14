import {createRouter, createWebHistory} from 'vue-router';
import {useAuthStore} from "@/store/auth";

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    meta: {isPublic: true},
    children: [
      {path: '', name: 'Home', component: () => import('@/views/Home.vue')},
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {requiresAuth: true}
      },
      {
        path: 'logout', name: 'Logout',
        component: () => import('@/views/Logout.vue'),
        meta: {requiresAuth: true}
      },
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: {isPublic: true}
      },
      {
        path: '/auth/callback',
        name: 'AuthCallback',
        component: () => import('@/views/AuthCallback.vue'),
        meta: {isPublic: true}
      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  // Optionally: Check the user's authentication status if it's not known.
  if (!auth.isAuthenticated) {
    await auth.checkAuthentication();
  }

  console.log('Routing from', from.fullPath, 'to', to.fullPath);

  if (to.meta.isPublic) {
    // If user is authenticated and tries to visit a public page (like Login), redirect to Dashboard.
    if (auth.isAuthenticated && to.name === 'Login') {
      next({name: 'Dashboard'});
    } else {
      next();
    }

  } else if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next({name: 'Login'});
  } else {
    next();
  }
});

export default router;
