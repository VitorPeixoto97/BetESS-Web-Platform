import Vue from 'vue'
import Router from 'vue-router'

import Auth from '@/components/pages/Auth'
import Jogos from '@/components/pages/Jogos'
import Jogo from '@/components/pages/Jogo'
import Stats from '@/components/pages/Stats'


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
    },
    {
      path: '/jogo',
      name: 'Jogo',
      component: Jogo
    },
    {
      path: '/stats',
      name: 'Stats',
      component: Stats
    }
  ]
})