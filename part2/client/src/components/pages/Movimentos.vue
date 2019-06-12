<template>
  <layout-basic>
    <div id="app">
      <div class="row main-row">
        <div class="column full-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row" style="height:100%;">
              <div class="column center-event">
                <p primary-title class="user-name"><b>Olá {{this.$session.get('user').name}}! </b></p>
              </div>
              <div class="column left-event"> </div>
              <div class="column right-event">
                <h5 class="teamname"><b>O seu saldo</b></h5>
                <h1 class="balance"><b>{{this.saldo}}€</b></h1>
              </div>
            </div>
          </v-card>
          </v-container>
        </div>
      </div>
      <div class="row main-row">
        <div class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row" style="height:100%;">
              <div class="column left-event">
                <p primary-title class="teamname"><b>Depositar</b></p>
              </div>
              <div class="column deposit">
                <div class="row">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountdepminus()">‒</button>
                  <input ref="valor" v-model="amountdep" class="amount" label="Valor"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountdepplus()">+</button>

                  <button class="btn btn-lg text-uppercase btn-movim" @click="depositar()">DEPOSITAR</button>
                </div>
              </div>


            </div>
          </v-card>
          </v-container>
        </div>

        <div class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row" style="height:100%;">
              <div class="column left-event">
                <p primary-title class="teamname"><b>Levantar</b></p>
              </div>
              <div class="column deposit">
                <div class="row">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountwitminus()">‒</button>
                  <input ref="valor" v-model="amountwit" class="amount" label="Valor"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountwitplus()">+</button>

                  <button class="btn btn-lg text-uppercase btn-movim" @click="levantar()">LEVANTAR</button>
                </div>
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
  name: 'Movimentos',
  components: {
    LayoutBasic,
  },
  data() {
      return {
        amountdep: 1,
        amountwit: 1,
        saldo: 0,
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  updated: function() {
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/user/info/" + this.$session.get('user_mail') + "/").then(response => {
        this.$session.set('user', response.data);
        this.saldo = response.data.coins;
      });
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    amountdepminus(){
      if(this.amountdep>1)
        this.amountdep = this.amountdep-1
    },
    amountdepplus(){
      this.amountdep = this.amountdep+1
    },

    amountwitminus(){
      if(this.amountwit>1)
        this.amountwit = this.amountwit-1
    },
    amountwitplus(){
      this.amountwit = this.amountwit+1
    },

    depositar(){
      axios.get("http://localhost:8005/user/add_coins/" + this.$session.get('user').id + "/" + this.amountdep + "/").then(response => {
        this.$notify({
          group: 'foo',
          type: 'success',
          title: 'Notificação',
          text: 'Quantia depositada!'
        });
      }).catch(e => {
        this.$notify({
          group: 'foo',
          type: 'error',
          title: 'Notificação',
          text: 'Ocorreu um erro. Tente mais tarde.'
        });
      });
      this.$forceUpdate();
      this.amountdep=1;
    },
    levantar(){
      axios.get("http://localhost:8005/user/remove_coins/" + this.$session.get('user').id + "/" + this.amountwit + "/").then(response => {
        this.$notify({
          group: 'foo',
          type: 'success',
          title: 'Notificação',
          text: 'Quantia levantada!'
        });
      }).catch(e => {
        this.$notify({
          group: 'foo',
          type: 'error',
          title: 'Erro',
          text: 'Ocorreu um erro. Tente mais tarde.'
        });
      });
      this.$forceUpdate();
      this.amountwit=1;
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

