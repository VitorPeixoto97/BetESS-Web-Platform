<template>
  <layout-basic>
    <div id="app" style="padding-bottom:100px;">
      <div class="row main-row">
        <div v-for="aposta in apostas" v-if="get(aposta.event).status==false" class="column main-column">
          <v-container text-xs-center>
            <v-card color="white" class="my-card event">
              <button v-if="aposta.profit==0" class="btn btn-lg text-uppercase btn-red"></button>
              <button v-if="aposta.profit>0" class="btn btn-lg text-uppercase btn-green"></button>
              <div class="row">
                <div class="column left-event">
                  <img class="crest" :src="get(aposta.event).equipaCsimb">
                  <p primary-title class="teamname"><b>{{get(aposta.event).equipaC}}</b></p>
                </div>
                <div class="column center-event">
                  <h5 class="teamname" style="color:#888;">{{get(aposta.event).competition}} | {{get(aposta.event).date}} | {{get(aposta.event).time}}</h5>
                  <h5 style="text-align:center; font-size:35px; padding:0px; margin:-10px 0px -5px 0px;"><b>{{get(aposta.event).result}}</b></h5>
                  <h5 class="teamname" v-if="aposta.result==0">{{get(aposta.event).equipaC}} | {{aposta.amount}}€ x {{aposta.odd}} = <b>{{aposta.profit}}€</b></h5>
                  <h5 class="teamname" v-if="aposta.result==1">Empate | {{aposta.amount}}€ x {{aposta.odd}} = <b>{{aposta.profit}}€</b></h5>
                  <h5 class="teamname" v-if="aposta.result==2">{{get(aposta.event).equipaF}} | {{aposta.amount}}€ x {{aposta.odd}} = <b>{{aposta.profit}}€</b></h5>
                
                </div>
                <div class="column right-event">
                  <img class="crest" :src="get(aposta.event).equipaFsimb">
                  <p primary-title class="teamname"><b>{{get(aposta.event).equipaF}}</b></p>
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
      eventos: null,
      new_apostas: [],
    }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/betting/bets/" + this.$session.get('user').id + "/").then(response => {
        this.apostas = response.data
      });
      axios.get("http://localhost:8005/matches/events/").then(response => {
        this.eventos = response.data;
      });
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },
    get(apostaevento){
      var i=0;
      while(i<this.eventos.length){
        if(this.eventos[i].id==apostaevento){
          var dadosevento = {
            competition: this.eventos[i].competition,
            type: this.eventos[i].type,
            oddV: this.eventos[i].oddV,
            oddE: this.eventos[i].oddE,
            oddD: this.eventos[i].oddD,
            equipaC: this.eventos[i].equipaC,
            equipaF: this.eventos[i].equipaF,
            equipaCsimb: this.eventos[i].equipaCsimb,
            equipaFsimb: this.eventos[i].equipaFsimb,
            status: this.eventos[i].status,
            date: this.eventos[i].date,
            time: this.eventos[i].time,
            result: this.eventos[i].result
          }
        }
        ++i;
      }
      return dadosevento;
    },

    cancelBet(aposta){
      axios.get("http://localhost:8005/user/add_coins/" + this.$session.get('user').id + "/" + aposta.amount + "/").then(response => {
        axios.get("http://localhost:8005/betting/del_bet/" + aposta.id + "/").then(response => {
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Aposta removida! O seu dinheiro foi reembolsado.'
          });
        }).catch(e => {});
      }).catch(e => {
        this.$notify({
          group: 'foo',
          type: 'error',
          title: 'Erro',
          text: 'Ocorreu um erro. Tente mais tarde.'
        });
      });

      this.FetchData();
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

