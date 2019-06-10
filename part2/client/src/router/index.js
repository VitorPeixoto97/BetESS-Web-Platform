import Vue from 'vue'
import Router from 'vue-router'

import Auth from '@/components/pages/Auth'
import Jogos from '@/components/pages/Jogos'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/jogos',
      name: 'Jogos',
      component: Jogos
    },
    {
      path: '/auth',
      name: 'Auth',
      component: Auth
    }
  ]
})