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
                <p class="teamname" v-if="selected.bet=='N' || jogo.id!=selected.id"><b>{{jogo.competition}}</b> | {{jogo.date}} | {{jogo.time}}</p>
                <p class="teamname" v-if="selected.bet!='N' && jogo.id==selected.id"><b>{{selected.equipa}}</b> | {{selected.odd}}</p>

                <div class="row" v-if="selected.bet!='N' && jogo.id==selected.id">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountminus()">‒</button>
                  <input ref="valor" v-model="selected.amount" class="amount" label="Valor da aposta"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountplus()">+</button>

                  <button class="btn btn-lg text-uppercase btn-bet" @click="apostar()">APOSTAR</button>
                </div>
                <div class="row" v-if="selected.bet=='N' || jogo.id!=selected.id">
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
          selected: {
            amount: 1,
            bet: "N",
            odd: 0,
            id: 0,
            equipa: "N",
            user: this.$session.get('user_email')
          }
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
      axios.get("http://localhost:8005/user/info/" + this.$session.get('user_email') + "/").then(response => {
        this.$session.set('user', response.data);
      });
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
      this.selected.amount = 1
      this.selected.bet = "V"
      this.selected.odd = odd
      this.selected.id = jogoid
      this.selected.equipa = equipa
    },
    betselectE(odd, jogoid){
      this.selected.amount = 1
      this.selected.bet = "E"
      this.selected.odd = odd
      this.selected.id = jogoid
      this.selected.equipa = "Empate"
    },
    betselectD(odd, jogoid, equipa){
      this.selected.amount = 1
      this.selected.bet = "D"
      this.selected.odd = odd
      this.selected.id = jogoid
      this.selected.equipa = equipa
    },

    amountminus(){
      if(this.selected.amount>1)
        this.selected.amount = this.selected.amount-1
    },
    amountplus(){
      if(this.selected.amount<50)
        this.selected.amount = this.selected.amount+1
    },

    apostar() {
      axios.post("http://localhost:8005/bet/", JSON.stringify(this.selected)).then(response => {

        }).catch(e => {});
        
        console.log("refreshh");
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

