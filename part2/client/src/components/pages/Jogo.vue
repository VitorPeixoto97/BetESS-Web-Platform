<template>
  <layout-basic>
    <div id="app">
      <v-container text-xs-center>
          <v-card color="white" class="my-card score">
            <div class="row">
              <div class="column">
                <img class="crest" :src="jogo.logoMe">
                <p primary-title class="justify-center teamname"><b>{{jogo.clube_nome}}</b></p>
              </div>
              <div class="column">
                <p v-if="started && this.jogo.resultado=='' " primary-title class="justify-center resultado"><b>0-0</b>
                <p v-if="this.eventos.length > 0" primary-title class="justify-center resultado"><b>{{jogo.resultado}}</b>
                <p v-if="this.eventos.length == 0" primary-title class="justify-center resultado"><b> </b>
                <p v-if="!started" class="justify-center datahora"><b>{{jogo.data}}</b></p>
                <p v-if="!started" class="justify-center datahora" style="margin-top:-15px;"><b>{{jogo.hora}}</b></p>
                <p v-if="!started" class="justify-center datahora"><b>{{jogo.casa}}</b></p>
                <p v-if="started" class="justify-center time"><b>{{ this.parte }}P | {{ this.minutos < 10 ? '0' + this.minutos : this.minutos }}:{{ this.segundos < 10 ? '0' + this.segundos : this.segundos }}</b></p>
              </div>
              <div class="column">
                <img class="crest" :src="jogo.logoAdv">
                <p primary-title class="justify-center teamname"><b>{{jogo.adv_nome}}</b></p>
              </div>
            </div>
          </v-card>
      </v-container>

      <v-container text-xs-center>
          <v-card color="white" class="my-card timer">
            <div class="row">
              <div class="column" style="margin:auto">
                <p class="justify-center" style="margin:auto">
                  <button class="btn btn-lg btn-primary btn-block text-uppercase btn-timer" style="margin:auto" v-on:click="updateClock()" :disabled="change || timer == 0">{{ paused ? 'Iniciar' : 'Parar' }}</button>
                </p>
              </div>
              <div class="column" style="margin:auto">
                <p class="justify-center" style="margin:auto">
                  <button class="btn btn-lg btn-primary btn-block text-uppercase btn-timer" style="margin:auto" v-on:click="changeClock()" :disabled="!paused || interval == null">{{ this.change ? 'Confirmar' : 'Alterar' }}</button>
                </p>
              </div>
            </div>
          </v-card>
      </v-container>

      <v-container text-xs-center v-if="change">
          <v-card color="white" class="my-card timechange">
            <p class="justify-center" style="font-size: x-large;">
              <plusminsfield v-model="clockChange.minutos" :min="0" :max="19"></plusminsfield> : 
              <plusminsfield v-model="clockChange.segundos" :min="0" :max="59"></plusminsfield>
            </p>
            <p class="justify-center" style="font-size: x-large;">
              <plusminsfield style="margin-left:6%" v-model="clockChange.parte" :min="1" :max="2"></plusminsfield>ª Parte
            </p>
          </v-card>
      </v-container>

      <v-container text-xs-center v-else>
        <div class="row v-row">
          <div class="column v-column">
            <v-flex dist distleft>
              <v-card color="white" class="my-card">
                <div class="column">
                  <form class="review-form" @submit.prevent="submitForm">
                    <div class="field">

                      <input v-model="tipo" autofocus class="input" ref="tipo" type="text" placeholder="Tipo de evento" v-on:keydown.down="selectType" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=true, selE=false, selA1=false, selA2=false, selC=false, selB=false">
                      <input v-model="evento.equipa" class="input" type="text" placeholder="Equipa" v-if="this.tipo_evento!=null && this.tipo_evento.equipa" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=true, selA1=false, selA2=false">
                      <input v-model="evento.atleta1" class="input" type="text" placeholder="Atleta" v-if="this.tipo_evento!=null && this.tipo_evento.atleta1" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=false, selA1=true, selA2=false, selC=false, selB=false, getAtletas1()">
                      <input v-model="evento.atleta2" class="input" type="text" placeholder="Atleta 2" v-if="this.tipo_evento!=null && this.tipo_evento.atleta2" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=false, selA1=false, selA2=true, selC=false, selB=false, getAtletas2()">
                      <input v-model="evento.zonaC" class="input" type="text" placeholder="Zona de campo" v-if="this.tipo_evento!=null && this.tipo_evento.zonaCampo" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=false, selA1=false, selA2=false, selC=true, selB=false">
                      <input v-model="evento.zonaB" class="input" type="text" placeholder="Zona da baliza" v-if="this.tipo_evento!=null && this.tipo_evento.zonaBaliza" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=false, selA1=false, selA2=false, selC=false, selB=true">
                      <input v-model="evento.novoinst" class="input" type="text" placeholder="Novo instante" v-if="this.tipo_evento!=null && this.tipo_evento.novoinstante" v-on:keyup.down="$event.target.nextElementSibling.focus()" v-on:keyup.up="$event.target.previousElementSibling.focus()" v-on:focus="selT=false, selE=false, selA1=false, selA2=false, selC=false, selB=false">
                      <input type="submit" value="Submit" hidden>
                    </div>
                  </form>
                </div>
              </v-card>
            </v-flex>
        </div>
          <div class="column v-column">
            <v-flex dist distright style="margin:auto">
              <v-card color="white" class="my-card">
                <div class="row">
                  <div class="column">
                    <p primary-title class="justify-center"><b>Sugestões de input</b></p>
                    <div v-if="selT">
                      <li v-for="sugestao in sugestaoTipos">
                        <b>{{sugestao.id}}</b> {{sugestao.tipo}}
                      </li>
                    </div>
                    <div v-if="selE">
                      <li>
                        <b>{{jogo.formacao}}</b> minha equipa
                      </li>
                      <li>
                        <b>{{jogo.adversario}}</b> adversario
                      </li>
                    </div>
                    <div v-if="selA1">
                      <li v-for="sugestao in sugestaoAtletas1">
                        <b>{{sugestao.id}}</b> {{sugestao.nome}} ({{sugestao.camisola}})
                      </li>
                    </div>
                    <div v-if="selA2">
                      <li v-for="sugestao in sugestaoAtletas2">
                        <b>{{sugestao.id}}</b> {{sugestao.nome}} ({{sugestao.camisola}})
                      </li>
                    </div>
                    <div v-if="selC">
                      <img src="../../assets/grids/8x4_alt.png" v-if="jogo.grelhaCampo == '8x4'" style="width: 90%">
                    </div>
                    <div v-if="selB">
                      <img src="../../assets/grids/2x2.png" v-if="jogo.grelhaBaliza == '2x2'" style="width: 50%">
                      <img src="../../assets/grids/2x3.png" v-if="jogo.grelhaBaliza == '2x3'" style="width: 50%">
                      <img src="../../assets/grids/3x3.png" v-if="jogo.grelhaBaliza == '3x3'" style="width: 50%">
                    </div>
                  </div>
                </div>
              </v-card>
            </v-flex>
          </div>
          
          
        </div>
      </v-container>

      <v-container text-xs-center>
          <v-card color="white" class="my-card eventos-table">
            <md-table v-model="searched" md-sort="name" md-sort-order="asc"  md-fixed-header ref="table">
              <md-table-toolbar>
                <div class="md-toolbar-section-start">
                  <h1 class="md-title"> </h1>
                </div>

                <md-field md-clearable class="md-toolbar-section-end">
                  <md-input placeholder="Pesquisar..." v-model="search" @input="searchOnTable" />
                </md-field>
              </md-table-toolbar>

              <md-table-empty-state
                md-label="Sem eventos"
                :md-description="'Ainda não tem eventos registados para este jogo.'">
              </md-table-empty-state>

              <md-table-row slot="md-table-row" slot-scope="{ item }" style="cursor:pointer" @click="verJogo(item.id, item.resultado)">
                <md-table-cell md-label="Instante" md-sort-by="instante">{{ item.instante }}</md-table-cell>
                <md-table-cell md-label="Equipa" md-sort-by="equipa">{{ item.equipa }}</md-table-cell>
                <md-table-cell md-label="Tipo de Evento" md-sort-by="tipo">{{ item.tipo }}</md-table-cell>
                <md-table-cell md-label="Atleta 1" md-sort-by="atleta1">{{ item.atleta1 }}</md-table-cell>
                <md-table-cell md-label="Atleta 2" md-sort-by="atleta2">{{ item.atleta2 }}</md-table-cell>
                <md-table-cell md-label="Timestamp" md-sort-by="timestamp">{{ item.timestamp }}</md-table-cell>
              </md-table-row>
            </md-table>
          </v-card>
      </v-container>
    </div>
  </layout-basic>
</template>

<script> 
import router from "../../router";
import LayoutBasic from '../layouts/Basic.vue'
import PlusMinusField from '../helpers/PlusMinusField.vue'
import axios from 'axios';
const toLower = text => {
  return text.toString().toLowerCase()
}
const searchByName = (items, term) => {
  if (term) {
    return items.filter(item => toLower(item.tipo).includes(toLower(term)))
  }
  return items
}
export default {
  name: 'Jogo',
  components: {
      LayoutBasic,
      'plusminsfield': PlusMinusField
  },
  data() {
    return {
      jogo: null,
      sugestaoTipos: null,
      sugestaoAtletas1: null,
      sugestaoAtletas2: null,
      bug: 'oh',
      
      search: null,
      searched: [],

      selT: false,
      selE: false,
      selA1: false,
      selA2: false,
      selC: false,
      selB: false,

      eventos_jogo: null,
      tipo: null,
      tipo_evento: null,

      evento: {
        jogo: this.jogo,
        equipa: null,
        tipo: null,
        atleta1: null,
        atleta2: null,
        zonaC: null,
        zonaB: null,
        instante: null,
        novoinst: null,
      },

      timer: 2400,
      started: false,
      parte: 1,
      minutos: 20,
      segundos: 0,
      paused: true,
      interval: null,
      change: false,
      clockChange: {
        minutos: 0,
        segundos: 0,
        parte: 1,
      }
    }
  },
  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },
  methods: {
    FetchData: function() {
      var app = this;
      axios.get(process.env.API_URL + "/server/get_jogo/"+this.$session.get('jogoTab')+"/").then(response => {
        app.jogo = response.data;
        app.evento.jogo = app.jogo.id;
      });
      axios.get(process.env.API_URL + "/server/get_eventos/"+this.$session.get('jogoTab')+"/").then(response => {
        app.eventos = response.data;
        this.searched = this.eventos;
      });
      axios.get(process.env.API_URL + "/server/get_tipos_selecionados/" + this.$session.get('user_email') + "/").then(response => {
        app.sugestaoTipos = response.data;
      });
    },

    updateTable() {
      var app = this;
      axios.get(process.env.API_URL + "/server/get_eventos/"+this.$session.get('jogoTab')+"/").then(response => {
        app.eventos = response.data;
        this.searched = this.eventos;
      });
    },

    updateJogo() {
      var app = this;
      axios.get(process.env.API_URL + "/server/get_jogo/"+this.$session.get('jogoTab')+"/").then(response => {
        app.jogo = response.data;
      });

    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    searchOnTable () {
      this.searched = searchByName(this.eventos, this.search)
    },

    verJogo(id) {
      this.$session.set('jogoTab', id)
      router.push("/jogo")
    },

    selectType() {
      var app = this;
      axios.get(process.env.API_URL + "/server/get_tipo_evento/" + app.tipo + "/").then(response => {
        app.tipo_evento = response.data;
        console.log(app.tipo_evento)
        app.evento.tipo = app.tipo_evento.id;
      })
    },

    allFieldsOk() {
      if (this.tipo_evento == null || (this.tipo_evento.equipa && (this.evento.equipa == null)) || (this.tipo_evento.atleta1 && (this.evento.atleta1 == null)) || (this.tipo_evento.atleta2 && (this.evento.atleta2 == null)) || (this.tipo_evento.zonaCampo && (this.evento.zonaC == null)) || (this.tipo_evento.zonaBaliza && (this.evento.zonaB == null)) || (this.tipo_evento.novoinstante && (this.evento.novoinst == null))) {
        return false;
      }

      return true;
    },

    submitForm() {
      /*
      if(this.evento.tipo != clockchange)
        this.evento.instante = this.timer;
      */

      if(this.allFieldsOk()){
        var app = this;
        axios.post(process.env.API_URL + "/server/evento/", JSON.stringify(app.evento)).then(response => {
          router.push("/jogo")
          this.updateTable();
          this.updateJogo();
          this.tipo=null;
          this.evento.equipa=null;
          this.evento.tipo=null;
          this.evento.atleta1=null;
          this.evento.atleta2=null;
          this.evento.zonaC=null;
          this.evento.zonaB=null;
          this.instante=null;
          this.novoinst=null;
          this.$refs.tipo.focus();
        }).catch(e => {});
        
        console.log("refreshh");
      }
    },

    getAtletas1() {
      if(this.evento.equipa != null){
        var app = this;

        axios.get(process.env.API_URL + "/server/get_atletas_campo/" + app.evento.equipa + "/" + app.evento.jogo + "/").then(response => {
          app.sugestaoAtletas1 = response.data
        })
      }
    },

    getAtletas2() {
      if(this.evento.equipa != null){
        var app = this;

        axios.get(process.env.API_URL + "/server/get_atletas_suplentes/" + app.evento.equipa + "/" + app.evento.jogo + "/").then(response => {
          app.sugestaoAtletas2 = response.data
        })
      }
    },

    updateClock(){
      this.started=true;
      if (!this.paused) { // está prestes a parar
        clearInterval(this.interval);
        console.log(this.evento);
        /* 
        this.evento.tipo = stop;
        this.evento.instante = this.timer;
        submitForm();
         */
      } else { // está prestes a (re)começar
        console.log('timer starts');
        /* 
        this.evento.tipo = start;
        this.evento.instante = this.timer;
        submitForm();
        */
        this.interval = setInterval(() => this.incrementTime(), 1000);
      }
      this.paused = !this.paused;
    },
    
    incrementTime() {
      if(this.timer > 0)
        this.timer -= 1;
      if(this.segundos == 0){
        if(this.minutos == 0){
          this.paused = true;
          clearInterval(this.interval);
          if(this.parte == 1){
            this.parte += 1;
            this.minutos = 20;
            /*
            this.evento.tipo = 2parte;
            this.instante = this.timer;
            submitForm();
            */
          }
          else {
            /*
            this.evento.tipo = fim;
            this.instante = this.timer;
            submitForm();
            */
          }
        }
        else{
          this.minutos -= 1;
          this.segundos = 59;
        }
      }
      else
        this.segundos -= 1;
    },

    changeClock(){
      if(!this.change) { //inicio de alteração
        this.clockChange.minutos = this.minutos;
        this.clockChange.segundos = this.segundos;
        this.clockChange.parte = this.parte;
      }
      else { //fim de alteração
          this.evento.instante = this.timer;
          this.timer = this.clockChange.minutos * 60 + this.clockChange.segundos;
          if(this.clockChange.parte == 1) this.timer += 1200;

          this.evento.novoinst = this.timer;
          this.minutos = this.clockChange.minutos;
          this.segundos = this.clockChange.segundos;
          this.parte = parseInt(this.clockChange.parte);

          /*
          this.evento.tipo = changeclock;
          submitForm();
          */
      }
      this.change = !this.change;
    }
  }
}
</script>

<style src="../../../dist/static/css/jogo.css">
</style>
