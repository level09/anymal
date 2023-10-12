import {createRouter, createWebHistory} from 'vue-router'
import api from '@/api';

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
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
})

router.beforeEach((to, from, next) => {

  if (to.meta.isPublic) {
    next();
  } else if (to.meta.requiresAuth) {
    // Here, perform an axios request to check whether the user session is active

    api.get('/check-session')
      .then(() => {
        next();
      })
      .catch(() => {
        next({ name: 'Login' });
      });

  } else {
    next();
  }
});

export default router;
