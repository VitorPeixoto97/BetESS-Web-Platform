<template>
  <layout-basic>
    <div id="app">
      <div class="row main-row">
        <div class="column full-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row" style="height:100%;">
              <div class="column left-event">
                <img class="crest" src=" ">
                <p primary-title class="teamname"><b> </b></p>
              </div>
              <div class="column center-event">
  
              
                <div class="row">
                  <button class="btn btn-lg text-uppercase btn-odd">odd</button>
                  <button class="btn btn-lg text-uppercase btn-odd">odd</button>
                  <button class="btn btn-lg text-uppercase btn-odd">odd</button>
                </div>
              </div>
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
            <div class="row">
              <div class="column left-event">
                <p primary-title class="teamname"><b>eC</b></p>
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

        <div class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <p primary-title class="teamname"><b>eC</b></p>
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
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

