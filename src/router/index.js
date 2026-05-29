import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/',                          component: () => import('../pages/HomePage.vue') },
  { path: '/signup',                    component: () => import('../pages/SignupPage.vue') },
  { path: '/events/:slug',              component: () => import('../pages/EventPage.vue') },
  { path: '/events/:slug/register',     component: () => import('../pages/RegisterPage.vue') },
  { path: '/login',                     component: () => import('../pages/LoginPage.vue') },
  { path: '/dashboard',                 component: () => import('../pages/DashboardPage.vue') },
  { path: '/admin/login',               component: () => import('../pages/AdminLoginPage.vue') },
  { path: '/admin/2fa',                 component: () => import('../pages/Admin2FAPage.vue') },
  { path: '/admin/dashboard',           component: () => import('../pages/AdminDashboardPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router
