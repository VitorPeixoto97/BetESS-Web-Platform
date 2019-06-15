<template>
  <admin-layout>
    <div id="app">
        <div class="row">
            <div class="column" align="center">
                <v-container text-xs-center>
                  <v-card color="white" class="my-card event">
                    <v-layout row>
                        <div class="column left-event">
                            <multiselect v-model="novo_evento.competicao" track-by="id" label="name" :searchable="false"
                                         placeholder="Competição" :close-on-select="true" :show-labels="false"
                                         :options="competicoes" :allow-empty="false" @input="selectCompetition()"></multiselect>
                                         
                            <multiselect v-model="novo_evento.equipaC" track-by="id" label="name" :searchable="false"
                                        placeholder="Equipa Casa" :close-on-select="true" :show-labels="false"
                                        :options="equipas" :allow-empty="false" :disabled="equipas.length==0">
                            </multiselect>

                            <input v-model.number="novo_evento.oddV" placeholder="1.00">
                        </div>
                        <div class="column center-event">
                            <input v-model.number="novo_evento.oddE" placeholder="1.00">
                            <button :disabled="!checkform()" class="btn btn-lg text-uppercase btn-bet" @click="newevento()">NOVO EVENTO</button>
                        </div>
                        <div class="column right-event">
                            <multiselect v-model="novo_evento.equipaF" track-by="id" label="name" :searchable="false"
                                        placeholder="Equipa Visitante" :close-on-select="true" :show-labels="false"
                                        :options="equipas" :allow-empty="false" :disabled="equipas.length==0">
                            </multiselect>
                            <input v-model.number="novo_evento.oddD" placeholder="1.00">
                        </div>
                        <div class="column center-event">
                            <datepicker v-model="data" placeholder="Select Date" format="yyyy-MM-dd" @change="selectDate()"></datepicker>
                            <vue-timepicker v-model="hora" placeholder="Select Time" format="HH:mm" @change="selectHour()" :minute-interval="5"></vue-timepicker>
                            <input type="checkbox" id="checkbox" :true-value="true" :false-value="false" v-model="novo_evento.premium">
                            <label for="checkbox">Evento Premium</label>
                        </div>
                    </v-layout>
                  </v-card>
                </v-container>
            </div>

        </div>

        <div v-for="evento in eventos" :key="evento.id" class="column main-column">
          <v-container text-xs-center>
          <v-card color="white" class="my-card event">
            <div class="row">
              <div class="column left-event">
                <img class="crest" :src="evento.equipaCsimb">
                <p primary-title class="teamname"><b>{{evento.equipaC}}</b></p>
              </div>
              <div class="column center-event">
                <p class="teamname"><b>{{evento.competition}}</b> | {{evento.date}} | {{evento.time}}</p>
                <div v-if="selected.id != 0 && evento.id == selected.id">
                    <input v-model="selected.result" placeholder="Resultado">
                    <button class="btn btn-lg text-uppercase btn-bet" :disabled="!checkresult()" @click="eventEnd()">CONFIRMAR</button>
                </div>
                <div class="column center-event" v-if="selected.id == 0 || evento.id != selected.id">
                    <!-- <button class="btn btn-lg text-uppercase btn-bet" @click="eventCancel(evento.id, evento.equipaC, evento.equipaF)">CANCELAR EVENTO</button> -->
                    <button class="btn btn-lg text-uppercase btn-end" @click="eventSelect(evento.id, evento.equipaC, evento.equipaF)">TERMINAR EVENTO</button>
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
  </admin-layout>
</template>

<script> 
import router from "../../router";
import AdminLayout from '../layouts/AdminLayout.vue'
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vuejs-timepicker'
import Multiselect from 'vue-multiselect'
import axios from 'axios';
export default {
  name: 'AdminEventos',
  components: {
    AdminLayout,
    Datepicker,
    VueTimepicker,
    Multiselect
  },
  data() {
    return {
      eventos: null,
      equipas: [],
      competicoes: [],
      data: null,
      hora: {
        HH: null,
        mm: null
      },

      selected: {
        id: 0,
        result: '',
        equipaC: '',
        equipaF: '',
      },

      novo_evento: {
          premium: false,
          competicao: null,
          equipaC: null,
          equipaF: null,
          oddV: null,
          oddE: null,
          oddD: null,
          data: '',
          hora:''
      },
        
    }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },

  methods: {
    FetchData: function() {
      axios.get("http://localhost:8005/matches/active_events/").then(response => {
        this.eventos = response.data;
        axios.get("http://localhost:8005/matches/competitions/").then(response => {
          this.competicoes = response.data;
        })
      })
      
      var aux = new Date();
      this.data = new Date(aux.getFullYear(), aux.getMonth(), aux.getDate())
      if(aux.getHours().toString().length < 2)
        this.hora.HH = '0' + aux.getHours()
      else this.hora.HH = aux.getHours()
      if(aux.getMinutes().toString().length < 2)
        this.hora.mm = '0' + Math.floor(aux.getMinutes()/5.0) * 5
      else this.hora.mm = Math.floor(aux.getMinutes()/5.0) * 5

      this.selectDate();this.selectHour()
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    eventSelect(id, equipaC, equipaF) {
        this.selected.id = id
        this.selected.equipaC = equipaC
        this.selected.equipaF = equipaF
    },

    eventCancel() {
      axios.get("http://localhost:8005/matches/bets/" + this.$session.get('user').id + "/").then(response => {})
    },

    eventEnd(){

        axios.post("http://localhost:8005/end_event/", JSON.stringify(this.selected)).then(response => {
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
        this.$router.go()
    },

    checkform() {
        return(this.novo_evento.equipaC != 0 && this.novo_evento.equipaF != 0 && this.novo_evento.equipaC != this.novo_evento.equipaF
        && this.novo_evento.oddV != null && this.novo_evento.oddE != null && this.novo_evento.oddD != null
        && this.novo_evento.oddV > 1 && this.novo_evento.oddE > 1 && this.novo_evento.oddD > 1
        && this.data != '' && this.hora != '')

    },

    checkresult() {
        var regex = RegExp('^\\s*\\d+-\\d+\\s*$');

        return regex.test(this.selected.result)
    },

    selectCompetition() {
        this.equipas = []
        axios.get("http://localhost:8005/matches/competition_teams/" + this.novo_evento.competicao.id + "/").then(response => {
          this.equipas = response.data;
        });
    },
    
    selectDate() {
        this.novo_evento.data = this.data.getFullYear() + '-' + (this.data.getMonth() + 1) + '-' + this.data.getDate()
    },

    selectHour() {
        this.novo_evento.hora = this.hora.HH + ':' + this.hora.mm
    },

    newevento() {
      axios.post("http://localhost:8005/event/", JSON.stringify(this.novo_evento)).then(response => {
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

