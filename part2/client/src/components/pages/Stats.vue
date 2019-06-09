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
                <p primary-title class="justify-center resultado"><b>{{jogo.resultado}}</b>
                <p class="justify-center datahora"><b>{{jogo.data}}</b></p>
                <p class="justify-center datahora" style="margin-top:-15px;"><b>{{jogo.hora}}</b></p>
                <p class="justify-center datahora"><b>{{jogo.casa}}</b></p>
              </div>
              <div class="column">
                <img class="crest" :src="jogo.logoAdv">
                <p primary-title class="justify-center teamname"><b>{{jogo.adv_nome}}</b></p>
              </div>
            </div>
          </v-card>
      </v-container>
      <v-container  text-xs-center>
        <v-card color="white" class="my-card chart">
          <img class="background" src="../../assets/logo.png"></img>
          <div id="chart">
            <apexchart type=bubble width=100% :options="chartOptions" :series="series" />
          </div>
        </v-card>
      </v-container>
    </div>
  </layout-basic>
</template>

<script> 
import router from "../../router";
import LayoutBasic from '../layouts/Basic.vue'
import axios from 'axios';
export default {
  name: 'Stats',
  components: {
    LayoutBasic,
  },
  data: function() {
    return {
      jogo: null,
      eventos: null,
      series: null,
      chartOptions: {
        grid: { show: false },
        dataLabels: {
          enabled: false
        },
        fill: {
          opacity: 0.8
        },
        colors: [this.$session.get('clube_cor'), this.$session.get('adv_cor'), '#FFFFFF00'],
        xaxis: {
          min: 0,
          max: 200,
          labels: { show:false },
          axisBorder: { show: false },
        },
        yaxis: {
          min: 0,
          max: 100,
        }
      }
    }
  },

  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
    this.bubbles();
  },

  methods: {
    FetchData: function() {
      var app = this;
      axios.get(process.env.API_URL + "/server/get_jogo/" + this.$session.get('jogoTab') + "/").then(response => {
        app.jogo = response.data;
        this.$session.set('jogo', response.data);
        this.$session.set('clube', response.data.clube_nome);
        this.$session.set('adv', response.data.adv_nome);
        this.$session.set('clube_cor', response.data.clube_cor);
        this.$session.set('adv_cor', response.data.adv_cor);
      })
      axios.get(process.env.API_URL + "/server/get_eventos/" + this.$session.get('jogoTab') + "/").then(response => {
        this.$session.set('eventos', response.data);
      })
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    verJogo(id) {
      this.$session.set('jogoTab', id)
      router.push("/jogo")
    },

    genBubbles(equipa) {
      var series = [];
      var i = 0;
      while(i < this.$session.get('eventos').length){
        if(this.$session.get('eventos')[i].equipa == equipa)
          series.push([this.$session.get('eventos')[i].gcx, this.$session.get('eventos')[i].gcy, this.$session.get('eventos')[i].size]);
        ++i;
      }
      return series;
    },

    bubbles() {
      this.series= [{
        name: this.$session.get('clube'),
        data: this.genBubbles(this.$session.get('clube'))
      },
      {
        name: this.$session.get('adv'),
        data: this.genBubbles(this.$session.get('adv'))
      }]
    }
  } 
}
</script>

<style src="../../../dist/static/css/stats.css">

