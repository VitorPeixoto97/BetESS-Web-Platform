import Vue from 'vue'
import Router from 'vue-router'

import Auth from '@/components/pages/Auth'
import Eventos from '@/components/pages/Eventos'
import Apostas from '@/components/pages/Apostas'
import Movimentos from '@/components/pages/Movimentos'
import Admin from '@/components/pages/Admin'
import Historico from '@/components/pages/Historico'

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
    },
    {
      path: '/movimentos',
      name: 'Movimentos',
      component: Movimentos
    },
    {
      path: '/historico',
      name: 'Histórico',
      component: Historico
    },
    {
      path: '/adminpage',
      name: 'Admin',
      component: Admin
    }
  ]
})