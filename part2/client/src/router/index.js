import Vue from 'vue'
import Router from 'vue-router'

import Auth from '@/components/pages/Auth'
import Eventos from '@/components/pages/Eventos'
import Apostas from '@/components/pages/Apostas'
import Registar from '@/components/pages/Registar'
import Historico from '@/components/pages/Historico'
import Movimentos from '@/components/pages/Movimentos'
import AdminEventos from '@/components/pages/AdminEventos'
import AdminEquipas from '@/components/pages/AdminEquipas'
import AdminHistorico from '@/components/pages/AdminHistorico'

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
      path: '/registar',
      name: 'Registar',
      component: Registar
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
      path: '/admineventos',
      name: 'AdminEventos',
      component: AdminEventos
    },
    {
      path: '/adminequipas',
      name: 'AdminEquipas',
      component: AdminEquipas
    },
    {
      path: '/adminhistorico',
      name: 'AdminHistorico',
      component: AdminHistorico
    }
  ]
})