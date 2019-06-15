<template>
  <admin-layout>
    <div id="app">
      <div class="row main-row">
        <div v-for="evento in eventos" v-if="evento.status==false" class="column main-column">
          <v-container text-xs-center>
            <v-card color="white" class="my-card event">
              <div class="row">
                <div class="column left-event">
                  <img class="crest" :src="evento.equipaCsimb">
                  <p primary-title class="teamname"><b>{{evento.equipaC}}</b></p>
                </div>
                <div class="column center-event">
                  <h5 class="teamname" style="color:#888;">{{evento.competition}} | {{evento.date}} | {{evento.time}}</h5>
                  <h5 style="text-align:center; font-size:35px; padding:0px; margin:-10px 0px -5px 0px;"><b>{{evento.result}}</b></h5>                
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
  </admin-layout>
</template>

<script> 
import router from "../../router";
import AdminLayout from '../layouts/AdminLayout.vue'
import axios from 'axios';
export default {
  name: 'AdminHistorico',
  components: {
    AdminLayout,
  },
  data() {
    return {
      eventos: null,
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

