<template>
  <layout-basic>
    <div id="app">
      <div class="row" style="margin:auto; width:60%;">
        <div v-for="jogo in jogos" class="column" style="width:50%; margin:30px auto auto auto">
          <v-container text-xs-center>
          <v-card color="white" class="my-card score">
            <div class="row">
              <div class="column" style="width:30%; margin:7px auto auto auto">
                <img class="crest" :src="jogo.equipaCsimb">
                <p primary-title class="teamname" style="margin-top:5px"><b>{{jogo.equipaC}}</b></p>
              </div>
              <div class="column" style="width:40%; margin:auto">
                <p class="teamname"><b>{{jogo.competition}}</b> | {{jogo.date}} | {{jogo.time}}</p>
                <button class="btn btn-lg text-uppercase btn-odd" @click="bet">{{jogo.oddV}}</button>
                <button class="btn btn-lg text-uppercase btn-odd" @click="login">{{jogo.oddE}}</button>
                <button class="btn btn-lg text-uppercase btn-odd" @click="login">{{jogo.oddD}}</button>
              </div>
              <div class="column" style="width:30%; margin:7px auto auto auto">
                <img class="crest" :src="jogo.equipaFsimb">
                <p primary-title class="teamname" style="margin-top:5px"><b>{{jogo.equipaF}}</b></p>
              </div>
            </div>
          </v-card>
          </v-container>
        </div>
      </div>
  

      

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

    bet(){

    },

  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

