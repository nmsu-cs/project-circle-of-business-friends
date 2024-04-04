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
    }
  ]
})

export default router
