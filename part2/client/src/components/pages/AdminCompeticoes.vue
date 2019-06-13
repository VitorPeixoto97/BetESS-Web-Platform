<template>
  <admin-layout>
    <div id="app">
        <div>
            <v-container text-xs-center>
            <v-card color="white" class="my-card event">
                <input v-model="nova_competicao.name" placeholder="Nova competicao...">
                <input v-model="nova_competicao.country" placeholder="País...">
                <button class="btn btn-lg text-uppercase btn-bet" :disabled="nova_competicao.name != null && nova_competicao.coutry != null" @click="competicao()">NOVA COMPETICAO</button>
            </v-card>
            </v-container>
        </div>

        <div v-for="competicao in competicoes" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <p primary-title class="teamname"><b>{{competicao.name}}</b></p>
              </div>
              <div class="column center-event">
                <p class="teamname"><b>{{competicao.country}}</b></p>
              </div>
              <!-- <div class="column right-event">
                <button class="btn btn-lg text-uppercase btn-bet" @click="deleteCompetition(competicao.id)">ELIMINAR COMPETICAO</button>
              </div> -->
            </div>
          </v-card>
          </v-container>
        </div>
    </div>
  </admin-layout>
</template>

<script> 
import router from "../../router";
import AdminLayout from '../layouts/AdminLayout.vue'
import axios from 'axios';
export default {
  name: 'AdminEventos',
  components: {
    AdminLayout,
  },
  data() {
      return {
          competicoes: null,

          nova_competicao: {
              name: '',
              country: ''
          },
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/matches/competitions/").then(response => {
        this.competitions = response.data;
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    deleteCompetition(id) {
      axios.get("http://localhost:8005/matches/del_competition/" + id + "/").then(response => {})
    },

    checkform() {
        return(this.nova_competicao.name != '' && this.nova_competicao.country != '')

    },

    competicao() {
        axios.post("http://localhost:8005/matches/add_competition", JSON.stringify(this.novo_evento)).then(response => {
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Evento registado.'
          });
          this.$router.go()
        }).catch(e => {
          this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Erro',
            text: e.response.data
          });
        });
    },


  } 
}
</script>

<style src="../../../dist/static/css/admin.css">

