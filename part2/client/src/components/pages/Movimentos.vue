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
                <h1 class="balance"><b>{{this.$session.get('coins')}}€</b></h1>
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
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountminus()">‒</button>
                  <input ref="valor" v-model="amount" class="amount" label="Valor"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountplus()">+</button>

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
            <div class="row">
              <div class="column left-event">
                <p primary-title class="teamname"><b>Levantar</b></p>
              </div>
              <div class="column center-event">

              </div>
              <div class="column right-event">
                <p primary-title class="teamname"><b>eF</b></p>
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
        amount: 1,
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/user/info/" + this.$session.get('user').email + "/").then(response => {this.$session.set('user', response.data);});
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    amountminus(){
      if(this.amount>1)
        this.amount = this.amount-1
    },
    amountplus(){
      this.amount = this.amount+1
    },

    depositar(){
      axios.get("http://localhost:8005/user/add_coins/" + this.$session.get('user').id + "/" + this.amount + "/").then(response => {
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
          title: 'Erro',
          text: e.response.data
        });
      });
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

