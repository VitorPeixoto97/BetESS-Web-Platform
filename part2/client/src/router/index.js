import Vue from 'vue'
import Router from 'vue-router'

import Auth from '@/components/pages/Auth'
import Eventos from '@/components/pages/Eventos'
import Apostas from '@/components/pages/Apostas'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/eventos',
      name: 'Eventos',
      component: Eventos
    },
    {
      path: '/auth',
      name: 'Auth',
      component: Auth
    },
    {
      path: '/apostas',
      name: 'Apostas',
      component: Apostas
    }
  ]
})