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
                <p class="teamname" v-if="selected_bet=='N' || jogo.id!=selected_id"><b>{{jogo.competition}}</b> | {{jogo.date}} | {{jogo.time}}</p>
                <p class="teamname" v-if="selected_bet!='N' && jogo.id==selected_id"><b>{{selected_equipa}}</b> | {{selected_odd}}</p>

                <div class="row" v-if="selected_bet!='N' && jogo.id==selected_id">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountminus()">‒</button>
                  <input ref="valor" v-model="amount" class="amount" label="Valor da aposta"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountplus()">+</button>

                  <button class="btn btn-lg text-uppercase btn-bet">APOSTAR</button>
                </div>
                <div class="row" v-if="selected_bet=='N' || jogo.id!=selected_id">
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectV(jogo.oddV, jogo.id, jogo.equipaC)">{{jogo.oddV}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectE(jogo.oddE, jogo.id)">{{jogo.oddE}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectD(jogo.oddD, jogo.id, jogo.equipaF)">{{jogo.oddD}}</button>
                </div>
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
import PlusMinusField from '../helpers/PlusMinusField.vue'
import axios from 'axios';
export default {
  name: 'Jogos',
  components: {
    LayoutBasic,
    'plusminsfield': PlusMinusField
  },
  data() {
      return {
          jogos: null,
          amount: 1,
          selected_bet: "N",
          selected_odd: 0,
          selected_id: 0,
          selected_equipa: "N",
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

    betselectV(odd, jogoid, equipa){
      this.amount = 1
      this.selected_bet = "V"
      this.selected_odd = odd
      this.selected_id = jogoid
      this.selected_equipa = equipa
    },
    betselectE(odd, jogoid){
      this.amount = 1
      this.selected_bet = "E"
      this.selected_odd = odd
      this.selected_id = jogoid
      this.selected_equipa = "Empate"
    },
    betselectD(odd, jogoid, equipa){
      this.amount = 1
      this.selected_bet = "D"
      this.selected_odd = odd
      this.selected_id = jogoid
      this.selected_equipa = equipa
    },

    amountminus(){
      if(this.amount>1)
        this.amount = this.amount-1
    },
    amountplus(){
      if(this.amount<50)
        this.amount = this.amount+1
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

