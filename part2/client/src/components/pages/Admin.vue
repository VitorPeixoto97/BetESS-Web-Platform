<template>
  <layout-basic>
    <div id="app">
        <div class="row main-row">
            <v-container text-xs-center>
            <v-card color="white" class="my-card event">
                <label class="typo__label">Equipa Casa</label>
                <multiselect v-model="novo_evento.competicao" track-by="id" label="name" placeholder="Select one" :options="competicoes" :allow-empty="false" @change="selectCompetition"></multiselect>
                <div class="row">
                    <label class="typo__label">Equipa Casa</label>
                    <multiselect v-model="novo_evento.equipaC" track-by="id" label="name" placeholder="Select one" :options="equipaOptions" :allow-empty="false"></multiselect>
                </div>
                <div class="row"><p>VS</p></div>
                <div class="row">
                    <label class="typo__label">Equipa Visitante</label>
                    <multiselect v-model="novo_evento.equipaF" track-by="id" label="name" placeholder="Select one" :options="equipaOptions" :allow-empty="false"></multiselect>
                </div>
                <div>
                    <div class="row">
                        <input v-model.number="novo_evento.oddV" placeholder="1.0">
                    </div>
                    <div class="row">
                        <input v-model.number="novo_evento.oddE" placeholder="1.0">
                    </div>
                    <div class="row">
                        <input v-model.number="novo_evento.oddD" placeholder="1.0">
                    </div>
                </div>
                <div>
                    <datepicker v-model="novo_evento.datepicker" placeholder="Select Date" @change="selectDate()"></datepicker>
                    <vue-timepicker v-model="novo_evento.hora" placeholder="Select Time" @change="selectHour()"></vue-timepicker>
                    <input type="checkbox" id="checkbox" v-model="novo_evento.premium">
                    <label for="checkbox">Evento Premium</label>
                    <button :disabled="checkform()" class="btn btn-lg text-uppercase btn-bet" @click="newevento()">NOVO EVENTO</button>
                </div>
            </v-card>
            </v-container>
        </div>
        
        <div class="row">
            <v-container text-xs-center>
            <v-card color="white" class="my-card event">
                <input v-model="nova_equipa.name" placeholder="Nova equipa...">
                <button class="btn btn-lg text-uppercase btn-bet" @click="equipa()">NOVA EQUIPA</button>
            </v-card>
            </v-container>
        </div>

        <div class="row">
            <v-container text-xs-center>
            <v-card color="white" class="my-card event">
                <input v-model="nova_competicao.name" placeholder="Nova competicao...">
                <input v-model="nova_competicao.country" placeholder="País...">
                <button class="btn btn-lg text-uppercase btn-bet" :disabled="nova_competicao.name != null && nova_competicao.coutry != null" @click="competicao()">NOVA COMPETICAO</button>
            </v-card>
            </v-container>
        </div>

        <div v-for="evento in eventos" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <img class="crest" :src="evento.equipaCsimb">
                <p primary-title class="teamname"><b>{{evento.equipaC}}</b></p>
              </div>
              <div class="column center-event">
                <p class="teamname"><b>{{evento.competition}}</b> | {{evento.date}} | {{evento.time}}</p>
                <input v-model.number="selected.result" placeholder="Resultado">
                <button class="btn btn-lg text-uppercase btn-bet" @click="matchEnd(evento.id, evento.equipaC, evento.equipaF)">TERMINAR EVENTO</button>
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
  </layout-basic>
</template>

<script> 
import router from "../../router";
import LayoutBasic from '../layouts/Basic.vue'
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vuejs-timepicker'
import axios from 'axios';
export default {
  name: 'Admin',
  components: {
    LayoutBasic,
    Datepicker,
    VueTimepicker
  },
  data() {
      return {
          eventos: null,
          equipas: null,
          competicoes: null,

          selected: {
            eventoid: 0,
            result: '',
            equipaC: '',
            equipaF: '',
          },

          nova_equipa: {
              nome: '',
              simbolo: ''
          },

          nova_competicao: {
              name: '',
              country: ''
          },

          novo_evento: {
              premium: false,
              competicao: 0,
              equipaC: 0,
              equipaF: 0,
              oddV: 0,
              oddE: 0,
              oddD: 0,
              data: '',
              hora: ''
          },

          datepicker: new Date(),
          timepicker: {
                  HH: null,
                  mm: null,
              },
          
          equipaOptions: [],
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
      })
      axios.get("http://localhost:8005/matches/teams/").then(response => {
        this.equipas = response.data;
      })
      axios.get("http://localhost:8005/matches/competitions/").then(response => {
        this.competitions = response.data;
      })
      aux = new Date();
      this.novo_evento.data = new Date(aux.getFullYear(), aux.getMonth(), aux.getDate())
      this.novo_evento.hora.HH = aux.getHours()
      this.novo_evento.hora.mm = aux.getMinutes()
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    matchEnd(eventoid, equipaC, equipaF){
        this.selected.id = eventoid
        this.selected.equipaC = equipaC
        this.selected.equipaF = equipaF

        axios.post("http://localhost:8005/matches/end_event/" + this.selected.id + "/" + this.selected.result + "/" + this.selected.equipaC + "/" + this.selected.equipaF, JSON.stringify(this.selected)).then(response => {
            this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Evento Terminado.'
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

    checkform() {
        return(this.novo_evento.equipaC != 0 && this.novo_evento.equipaF != 0 && this.novo_evento.equipaC != this.novo_evento.equipaF
        && this.novo_evento.oddV != 0 && this.novo_evento.oddE != 0 && this.novo_evento.oddD != 0
        && this.novo_evento.data != '' && this.novo_evento.hora != '')

    },

    selectCompetition() {
        this.equipaOptions = []
        this.equipas.forEach(equipa => {
            if (equipa.competicao == this.novo_evento.competicao)
                this.equipaOptions.push(equipa)
        });
    },
    
    selectDate() {
        this.novo_evento.data = this.datepicker.getFullYear() + '-' + this.datepicker.getMonth() + 1 + '-' + this.datepicker.getDate()
    },

    selectHour() {
        this.novo_evento.hora = this.timepicker.HH + ':' + this.timepicker.mm
    },

    newevento() {
        axios.post("http://localhost:8005/matches/add_event", JSON.stringify(this.novo_evento)).then(response => {
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Evento registado.'
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

