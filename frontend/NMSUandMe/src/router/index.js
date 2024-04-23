/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import index from '../pages/index.vue'
import signup from '../pages/signup.vue'
import profile from '../pages/profile.vue'
import user_portal from '../pages/user_portal.vue'
import login from '../pages/login.vue'
import matches from '../pages/matches'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  extendRoutes: setupLayouts,
  routes:[
    {
      path:'/',
      name:'index',
      component: index
    },
    {
      path:'/signup',
      name:'signup',
      component: signup
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path:'/profile',
      name: 'profile',
      component: profile
    },
    {
      path: '/user_portal',
      name: 'user_portal',
      component: user_portal
    },
    {
      path: '/matches',
      name: 'matches',
      component: matches
    }
  ]
})

export default router
