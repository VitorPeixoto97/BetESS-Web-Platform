<template>
  <layout-basic>
    <div id="app" style="padding-bottom:100px;">
      <div class="row main-row">
        <div v-for="evento in eventos" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <img class="crest" :src="evento.equipaCsimb">
                <p primary-title class="teamname"><b>{{evento.equipaC}}</b></p>
              </div>
              <div class="column center-event">
                <p class="teamname" v-if="selected.bet=='N' || evento.id!=selected.id"><b>{{evento.competition}}</b> | {{evento.date}} | {{evento.time}}</p>
                <p class="teamname" v-if="selected.bet!='N' && evento.id==selected.id"><b>{{selected.equipa}}</b> | {{selected.odd}}</p>

                <div class="row" v-if="selected.bet!='N' && evento.id==selected.id">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountminus()">‒</button>
                  <input ref="valor" v-model="selected.amount" class="amount" label="Valor da aposta"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountplus()">+</button>

                  <button class="btn btn-lg text-uppercase btn-bet" @click="apostar()">APOSTAR</button>
                </div>
                <div class="row" v-if="selected.bet=='N' || evento.id!=selected.id">
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectV(evento.oddV, evento.id, evento.equipaC)">{{evento.oddV}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectE(evento.oddE, evento.id)">{{evento.oddE}}</button>
                  <button class="btn btn-lg text-uppercase btn-odd" @click="betselectD(evento.oddD, evento.id, evento.equipaF)">{{evento.oddD}}</button>
                </div>
              </div>
              <div class="column right-event">
                <img class="crest" :src="evento.equipaFsimb">
                <p primary-title class="teamname"><b>{{evento.equipaF}}</b></p>
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
  name: 'Eventos',
  components: {
    LayoutBasic,
  },
  data() {
      return {
          eventos: null,
          selected: {
            amount: 1,
            bet: "N",
            odd: 0,
            id: 0,
            equipa: "N",
            user: null,
          }
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      this.selected.user = this.$session.get('user');
      axios.get("http://localhost:8005/user/info/" + this.$session.get('user').email + "/").then(response => {this.$session.set('user', response.data);});
      this.$session.set('coins', this.$session.get('user').coins);
      axios.get("http://localhost:8005/matches/events/" + this.$session.get('user').type + "/").then(response => {
        this.eventos = response.data;
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    betselectV(odd, eventoid, equipa){
      this.selected.amount = 1
      this.selected.bet = "V"
      this.selected.odd = odd
      this.selected.id = eventoid
      this.selected.equipa = equipa
    },
    betselectE(odd, eventoid){
      this.selected.amount = 1
      this.selected.bet = "E"
      this.selected.odd = odd
      this.selected.id = eventoid
      this.selected.equipa = "Empate"
    },
    betselectD(odd, eventoid, equipa){
      this.selected.amount = 1
      this.selected.bet = "D"
      this.selected.odd = odd
      this.selected.id = eventoid
      this.selected.equipa = equipa
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
      if(this.$session.get('coins')<this.selected.amount){
        this.$notify({
          group: 'foo',
          type: 'error',
          title: 'Erro',
          text: 'Não tem saldo suficiente para realizar a aposta!'
        });
      }
      else{
        axios.post("http://localhost:8005/bet/", JSON.stringify(this.selected)).then(response => {
          axios.get("http://localhost:8005/user/remove_coins/" + this.$session.get('user').id + "/" + this.selected.amount + "/").then(response => {}).catch(e => {});
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Aposta registada!'
          });
          this.$session.set('coins', this.$session.get('coins') - this.selected.amount)
        }).catch(e => {
          this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Erro',
            text: e.response.data
          });
        });
      }
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

