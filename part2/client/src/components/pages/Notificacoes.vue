<template>
  <layout-basic>
    <div id="app" style="padding-bottom:100px;">
      <div class="row main-row">
        <div v-for="notif in notifs" class="column main-column">
          <v-container text-xs-center>
            <v-card style="height:120px" class="my-card event">
              <button v-if="getAposta(notif.bet).profit==0" @click="readNotif(notif.id)" class="btn btn-lg text-uppercase btn-red btn-red-dismiss">✓</button>
              <button v-if="getAposta(notif.bet).profit>0" @click="readNotif(notif.id)" class="btn btn-lg text-uppercase btn-green btn-green-dismiss">✓</button>
              <div class="row">
                <div class="column left-event">
                  <img class="crest" style="margin-top:5px;" :src="get(getAposta(notif.bet).event).equipaCsimb">
                  <p primary-title class="teamname"><b>{{get(getAposta(notif.bet).event).equipaC}}</b></p>
                </div>
                <div class="column center-event">
                  <h5 class="teamname" style="color:#888;">{{get(getAposta(notif.bet).event).competition}} | {{get(getAposta(notif.bet).event).date}} | {{get(getAposta(notif.bet).event).time}}</h5>
                  <h5 style="text-align:center; font-size:35px; padding:0px; margin:-10px 0px -5px 0px;"><b>{{get(getAposta(notif.bet).event).result}}</b></h5>
                  <h5 class="teamname" v-if="getAposta(notif.bet).result==0">{{get(getAposta(notif.bet).event).equipaC}} | {{getAposta(notif.bet).amount}}€ x {{getAposta(notif.bet).odd}} = <b>{{getAposta(notif.bet).profit}}€</b></h5>
                  <h5 class="teamname" v-if="getAposta(notif.bet).result==1">Empate | {{getAposta(notif.bet).amount}}€ x {{getAposta(notif.bet).odd}} = <b>{{getAposta(notif.bet).profit}}€</b></h5>
                  <h5 class="teamname" v-if="getAposta(notif.bet).result==2">{{get(getAposta(notif.bet).event).equipaF}} | {{getAposta(notif.bet).amount}}€ x {{getAposta(notif.bet).odd}} = <b>{{getAposta(notif.bet).profit}}€</b></h5>
                
                </div>
                <div class="column right-event">
                  <img class="crest" style="margin-top:5px;" :src="get(getAposta(notif.bet).event).equipaFsimb">
                  <p primary-title class="teamname"><b>{{get(getAposta(notif.bet).event).equipaF}}</b></p>
                </div>
              </div>
              <div class="row" style="width:100%;">
                <h5 class="teamname" style="margin:auto; text-align:center;">{{notif.message}}</b></h5>
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
      notifs: null,
    }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/matches/events/").then(response => {
        this.eventos = response.data;
      });
      axios.get("http://localhost:8005/betting/notifs/" + this.$session.get('user').id + "/").then(response => {
        this.notifs = response.data;
      });
      axios.get("http://localhost:8005/betting/bets/" + this.$session.get('user').id + "/").then(response => {
        this.apostas = response.data;
      });
    },
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },
    getAposta(apostaid){
      var i=0;
      while(i<this.apostas.length){
        if(this.apostas[i].id==apostaid){
          var dadosaposta = {
            result: this.apostas[i].result,
            amount: this.apostas[i].amount,
            odd: this.apostas[i].odd,
            profit: this.apostas[i].profit,
            event: this.apostas[i].event
          }
        }
        ++i;
      }
      return dadosaposta;
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

    readNotif(notifid){
      axios.get("http://localhost:8005/betting/del_notif/" + notifid + "/").then(response => {
        this.aposta = response.data;
      });
      this.FetchData();
    }
  }
}
</script>

<style src="../../../dist/static/css/stats.css">

