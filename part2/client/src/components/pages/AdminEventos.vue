<template>
  <admin-layout>
    <div id="app" style="padding-bottom:100px;">
      <div class="row main-row" style="padding:0px 15px 0px 15px;">
        <div class="column full-column">
            <v-card  style="color:#FFF; height:240px;" class="my-card event">
              <v-container>
                
                <div class="row" style="width:98%; padding-top:30px; margin:auto;">
                  <multiselect v-model="novo_evento.competicao" track-by="id" label="name" :searchable="false"
                               placeholder="Competição" :close-on-select="true" :show-labels="false"
                               :options="competicoes" :allow-empty="false" style="width:30%;">
                  </multiselect>

                  <datepicker style="color:#333; width:15%;" v-model="data" :bootstrap-styling="true" placeholder="Select Date" format="yyyy-MM-dd" @change="selectDate()"></datepicker>
                  <vue-timepicker style="width:auto;"v-model="hora" placeholder="Select Time" format="HH:mm" @change="selectHour()" :minute-interval="5"></vue-timepicker>

                  <b-form-checkbox id="checkbox" class="checkbox-premium" v-model="novo_evento.premium" switch>
                    <label class="label-coins" style="margin:auto">Evento Premium</label>
                  </b-form-checkbox>

                </div>

                <div class="row" style="width:98%; padding-top:30px; margin:auto;">
                                         
                  <multiselect v-model="novo_evento.equipaC" track-by="id" label="name" :searchable="false"
                               placeholder="Equipa Casa" :close-on-select="true" :show-labels="false"
                               :options="equipas" :allow-empty="false" :disabled="equipas.length==0" style="width:25%;">
                  </multiselect>

                  <input v-model.number="novo_evento.oddV" class="form-control" placeholder="Odd 1" style="width:10%">
                  <input v-model.number="novo_evento.oddE" class="form-control" placeholder="Odd X" style="width:10%">
                  <input v-model.number="novo_evento.oddD" class="form-control" placeholder="Odd 2" style="width:10%">

                
                  <multiselect v-model="novo_evento.equipaF" track-by="id" label="name" :searchable="false"
                               placeholder="Equipa Visitante" :close-on-select="true" :show-labels="false"
                               :options="equipas" :allow-empty="false" :disabled="equipas.length==0" style="width:25%;">
                  </multiselect>
                  
                </div>
                <div class="row" style="width:98%; padding-top:30px; margin:auto;">
                  <button :disabled="!checkform()" class="btn btn-lg text-uppercase btn-movim" style="width:220px; margin:auto" @click="newevento()">ADICIONAR EVENTO</button>
                </div>
                  
                </v-container>
            </v-card>
        </div>

      </div>

      <div class="row main-row">
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
                    <input class="form-control" style="width:25%; display:inline" v-model="selected.result" placeholder="Resultado">
                    <button class="btn btn-lg text-uppercase btn-primary btn-confirm-score" :disabled="!checkresult()" @click="eventEnd()">CONFIRMAR</button>
                </div>
                <div class="row" v-if="selected.id == 0 || evento.id != selected.id">
                  <!-- <button class="btn btn-lg text-uppercase btn-bet" @click="eventCancel(evento.id, evento.equipaC, evento.equipaF)">CANCELAR EVENTO</button> -->
                  <button class="btn btn-lg text-uppercase btn-primary" @click="eventSelect(evento.id, evento.equipaC, evento.equipaF)">TERMINAR EVENTO</button>
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
        });
        axios.get("http://localhost:8005/matches/teams/").then(response => {
          this.equipas = response.data;
        });
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

        axios.post("http://localhost:8005/event_end/", JSON.stringify(this.selected)).then(response => {
          this.$notify({
            group: 'foo',
            type: 'success',
            title: 'Notificação',
            text: 'Evento terminado com sucesso.'
          });
        }).catch(e => {
            this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Erro',
            text: e.response.data
            });
        });
        this.FetchData();
    },

    checkform() {
        return(this.novo_evento.equipaC != null && this.novo_evento.equipaF != null && this.novo_evento.equipaC != this.novo_evento.equipaF
        && this.novo_evento.oddV>1 && this.novo_evento.oddE>1 && this.novo_evento.oddD>1
        && this.data != '' && this.hora != '')

    },

    checkresult() {
        var regex = RegExp('^\\s*\\d+-\\d+\\s*$');

        return regex.test(this.selected.result)
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

<style src="../../../dist/static/css/stats.css">

