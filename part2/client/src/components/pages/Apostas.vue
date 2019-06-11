
<template>
  <layout-basic>
    <div id="app">
      <div class="row main-row">
        <div v-for="aposta in apostas" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <img class="crest" src=" ">
                <p primary-title class="teamname"><b> Equipa Casa</b></p>
              </div>
              <div class="column center-event">
                <p class="teamname"><b>Competiçao</b> | Dia | Hora</p>

                <div class="row">
                  <button class="btn btn-lg text-uppercase btn-odd">{{aposta.result}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd">{{aposta.amount}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd">{{aposta.odd}}</button>
                </div>
              </div>
              <div class="column right-event">
                <img class="crest" src=" ">
                <p primary-title class="teamname"><b> Equipa Fora</b></p>
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
  name: 'Apostas',
  components: {
    LayoutBasic,
  },
  data() {
      return {
          apostas: null,
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      var app = this;
      axios.get("http://localhost:8005/betting/bets/" + this.$session.get('user').id + "/").then(response => {
        app.apostas = response.data
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


    amountminus(){
      if(this.selected.amount>1)
        this.selected.amount = this.selected.amount-1
    },
    amountplus(){
      if(this.selected.amount<50 && this.selected.amount<this.$session.get('user').coins)
        this.selected.amount = this.selected.amount+1
    },

    apostar() {
      axios.post("http://localhost:8005/bet/", JSON.stringify(this.selected)).then(response => {

        }).catch(e => {});
        
        console.log("refreshh");
        this.FetchData();
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

