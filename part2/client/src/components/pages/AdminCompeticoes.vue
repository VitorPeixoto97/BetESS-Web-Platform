<template>
  <admin-layout>
    <div id="app">
      <div class="column main-column">
        <v-container text-xs-center>
        <v-card color="white" class="my-card event">
          <div class="row main-row">
            <div class="column left-event" align="center">
              <input v-model="nova_competicao.name" placeholder="Nova competicao...">
            </div>
            <div class="column center-event" align="center">
              <input v-model="nova_competicao.country" placeholder="País...">
            </div>
            <div class="column right-event" align="center">
              <button class="btn btn-lg text-uppercase btn-end" :disabled="!checkform()" @click="competicao()">NOVA COMPETICAO</button>
            </div>
          </div>
        </v-card>
        </v-container>
      </div>

      <div class="row main-row">
        <div v-for="competicao in competicoes" :key="competicao.id" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <p primary-title class="teamname"><b>{{competicao.name}}</b></p>
                <div v-if="selected.id != -1 && competicao.id == selected.id && selected.option == 0">
                  <multiselect v-model="selected.equipa" track-by="id" label="name" :searchable="false" 
                              placeholder="Equipa" :close-on-select="true" :show-labels="false"
                              :options="equipas" :allow-empty="true"></multiselect>
                  <button class="btn btn-lg text-uppercase btn-end" :disabled="selected.equipa==null" @click="addTeam()">CONFIRMAR</button>
                </div>
                <div class="column center-event" v-if="selected.id == -1 || competicao.id != selected.id || selected.option != 0">
                    <button class="btn btn-lg text-uppercase btn-end" @click="selectCompetition(competicao.id, 0)">ASSOCIAR EQUIPA</button>
                </div>
              </div>
              <div class="column center-event">
                <p class="teamname"><b>{{competicao.country}}</b></p>
                <div v-if="selected.id != -1 && competicao.id == selected.id  && selected.option == 1">
                  <multiselect v-model="selected.equipa" track-by="id" label="name" :searchable="false"
                    placeholder="Equipa" :close-on-select="true" :show-labels="false" 
                    :options="equipas"  :allow-empty="true"></multiselect>
                  <button class="btn btn-lg text-uppercase btn-bet" :disabled="selected.equipa==null" @click="removeTeam()">CONFIRMAR</button>
                </div>
                <div class="column center-event" v-if="selected.id == -1 || competicao.id != selected.id  || selected.option != 1">
                    <button class="btn btn-lg text-uppercase btn-end" @click="selectCompetition(competicao.id, 1)">REMOVER EQUIPA</button>
                </div>
              </div>
              <!-- <div class="column right-event">
                <button class="btn btn-lg text-uppercase btn-bet" @click="deleteCompetition(competicao.id)">ELIMINAR COMPETICAO</button>
              </div> -->
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
import Multiselect from 'vue-multiselect'
import axios from 'axios';
export default {
  name: 'AdminEventos',
  components: {
    AdminLayout,
    Multiselect
  },
  data() {
      return {
          competicoes: null,
          equipas: [],

          nova_competicao: {
              name: '',
              country: ''
          },

          selected: {
            id: -1,
            option: -1,
            equipa: null,
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
        this.competicoes = response.data;
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    // deleteCompetition(id) {
    //   axios.get("http://localhost:8005/matches/del_competition/" + id + "/").then(response => {})
    // },

    selectCompetition(id, option) {
      if(option == 0)
          axios.get("http://localhost:8005/matches/not_competition_teams/" + id + "/").then(response => {
          this.equipas = response.data
          this.selected.id = id
          this.selected.option = option
          this.selected.equipa = null
        })
      else if(option == 1)
        axios.get("http://localhost:8005/matches/competition_teams/" + id + "/").then(response => {
          this.equipas = response.data
          this.selected.id = id
          this.selected.option = option
          this.selected.equipa = null
        })
    },

    checkform() {
      var valid = true
      if(this.nova_competicao.name != '' && this.nova_competicao.country != ''){
        for(var competicao in this.competicoes)
          if(competicao.name == this.nova_competicao.name && competicao.country == this.nova_competicao.country){
            valid = false
            break
          }
      }
      else valid = false
      return valid
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

    addTeam() {
      axios.get("http://localhost:8005/matches/add_comp_team/" + this.selected.id + "/" + this.selected.equipa.id + "/").then(response => {
        this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Equipa associada.'
          });
      }).catch(e => {
          this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Erro',
            text: e.response.data
          });
        });
        this.$router.go()
    },

    removeTeam() {
      axios.get("http://localhost:8005/matches/rem_comp_team/" + this.selected.id + "/" + this.selected.equipa.id + "/").then(response => {
        this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Equipa removida da competição.'
          });
      }).catch(e => {
          this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Erro',
            text: e.response.data
          });
        });
        this.$router.go()
    }
  } 
}
</script>

<style src="../../../dist/static/css/admin.css">

