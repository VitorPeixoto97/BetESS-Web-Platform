<template>
  <layout-basic>
    <div id="app">
      <v-container text-xs-center>
          <v-card color="white" class="my-card score">
            <div class="row">
              <div class="column">
                <img class="crest" src="jogo.logoMe">
                <p primary-title class="justify-center teamname"><b>casa</b></p>
              </div>
              <div class="column">
                <p class="justify-center datahora"><b>oddV</b></p>
                <p class="justify-center datahora"><b>oddE</b></p>
                <p class="justify-center datahora"><b>oddD</b></p>
              </div>
              <div class="column">
                <img class="crest" src="jogo.logoAdv">
                <p primary-title class="justify-center teamname"><b>fora</b></p>
              </div>
            </div>
          </v-card>
      </v-container>

    </div>
  </layout-basic>
</template>

<script> 
import router from "../../router";
import LayoutBasic from '../layouts/Basic.vue'
import axios from 'axios';
export default {
  name: 'Jogos',
  components: {
    LayoutBasic,
  },
  data() {
      return {
          jogos: null,
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      var app = this;
      axios.get("http://localhost:8005/matches/events/").then(response => {
        app.jogos = response.data
        this.$session.set('eventos', response.data);
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    verJogo(id) {
      this.$session.set('jogoTab', id)
      router.push("/jogo")
    },



  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

