<template>
  <admin-layout>
    <div id="app" style="padding-bottom:100px;">
      <div class="row main-row" style="padding:0px 15px 0px 15px;">
        <div class="column full-column">
          <v-card  style="color:#FFF; height:80px;" class="my-card event">
            <v-container>
              <div class="row inside-row">
                  <input class="form-control" style="width:25%;" v-model="nova_equipa.name" placeholder="Nome">
                
                  <input class="form-control" style="width:25%;" v-model="nova_equipa.simbolo" placeholder="Símbolo (URL)">
                
                  <button class="btn btn-lg text-uppercase btn-primary" style="display:inline; width:20%;" v-on:click="equipa()" :disabled="!checkform()">ADICIONAR EQUIPA</button>
              </div>
            </v-container>
          </v-card>
        </div>
      </div>

      <div class="row main-row" style="padding:0px 15px 0px 15px;">
        <div class="column full-column">
          <v-card  style="color:#FFF; height:80px;" class="my-card event">
            <v-container>
              <div class="row inside-row">
                  <input class="form-control" style="width:25%;" v-model="nova_competicao.name" placeholder="Nome">
                
                  <input class="form-control" style="width:25%;" v-model="nova_competicao.country" placeholder="País">
                
                  <button class="btn btn-lg text-uppercase btn-primary" style="display:inline; width:30%;" v-on:click="competicao()" :disabled="!checkformCompeticao()">ADICIONAR COMPETIÇÃO</button>
              </div>
            </v-container>
          </v-card>
        </div>
      </div>

      <div class="row main-row">
        <div v-for="equipa in equipas" class="column club-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column" style="margin:10px auto auto auto">
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

          nova_competicao: {
              name: '',
              country: ''
          }
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
        var imgregex = RegExp('^.+\.(jpeg|jpg|gif|png)$')
        return(imgregex.test(this.nova_equipa.simbolo))
    },
    checkformCompeticao() {
        if(this.nova_competicao.name.length>0 && this.nova_competicao.country.length>0)
          return true;
        else return false;
    },

    equipa() {
      axios.get(this.nova_equipa.simbolo).then( response => {
            axios.post("http://localhost:8005/team/", JSON.stringify(this.nova_equipa)).then(response => {
                this.$notify({
                    group: 'foo',
                    type: 'success',
                    title: 'Notificação',
                    text: 'Equipa registada.'
                });
                this.FetchData();
                this.nova_equipa.name='';
                this.nova_equipa.simbolo='';
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

    competicao() {
        axios.post("http://localhost:8005/competition/", JSON.stringify(this.nova_competicao)).then(response => {
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Competição registada.'
          });
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

<style src="../../../dist/static/css/stats.css">

