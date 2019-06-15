<template>
  <admin-layout>
    <div id="app">
      <div class="column main-column">
        <v-container text-xs-center>
        <v-card color="white" class="my-card event">
          <div class="row main-row">
            <div class="column left-event" align="center">
              <input v-model="nova_equipa.name" placeholder="Nova equipa...">
            </div>
            <div class="column center-event" align="center">
              <input v-model="nova_equipa.simbolo" placeholder="URL de logótipo...">
            </div>
            <div class="column right-event" align="center">
              <button class="btn btn-lg text-uppercase btn-end" v-on:click="equipa()" :disabled="!checkform()">NOVA EQUIPA</button>
            </div>
          </div>
        </v-card>
        </v-container>
      </div>

        <div v-for="equipa in equipas" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <img class="crest" :src="equipa.simbolo">
                <p primary-title class="teamname"><b>{{equipa.name}}</b></p>
              </div>
              <!-- <div class="column right-event">
                <button class="btn btn-lg text-uppercase btn-end" @click="deleteTeam(equipa.id)">ELIMINAR EQUIPA</button>
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
  name: 'AdminEquipas',
  components: {
    AdminLayout,
  },
  data() {
      return {
          equipas: null,

          nova_equipa: {
              name: '',
              simbolo: ''
          },
      }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/matches/teams/").then(response => {
        this.equipas = response.data;
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    // deleteTeam(id) {
    //   axios.get("http://localhost:8005/matches/del_team/" + id + "/").then(response => {})
    // },

    checkform() {
        var nameregex = RegExp('^[a-zA-z ]+$');
        var imgregex = RegExp('^.+\.(jpeg|jpg|gif|png)$')
        return(nameregex.test(this.nova_equipa.name) && imgregex.test(this.nova_equipa.simbolo))

    },

    equipa() {
        axios.get(this.nova_equipa.simbolo).then( response => {
            axios.post("http://localhost:8005/team/", JSON.stringify(this.nova_equipa)).then(response => {
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
        }).catch(response => {
            this.$notify({
                group: 'foo',
                type: 'error',
                title: 'Erro',
                text: 'Imagem inválida.'
            })
        })
    },


  } 
}
</script>

<style src="../../../dist/static/css/admin.css">

