// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import VueSession from 'vue-session'
import BootstrapVue from 'bootstrap-vue'
import VueMaterial from 'vue-material'
import mdbDatatable from 'mdbvue';
import VueApexCharts from 'vue-apexcharts'
import { MdButton, MdContent, MdTabs } from 'vue-material/dist/components'

import 'vuetify/dist/vuetify.min.css'
import 'jquery/dist/jquery.min.js';
import 'bulma/css/bulma.css';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

require('../dist/static/css/index.css')


Vue.use(MdButton)
Vue.use(MdContent)
Vue.use(MdTabs)
Vue.use(VueMaterial)
Vue.use(BootstrapVue)
Vue.use(Vuetify)
Vue.use(VueSession)
Vue.component('apexchart', VueApexCharts)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
