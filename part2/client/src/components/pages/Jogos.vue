<template>
  <layout-basic>
    <div id="app">
      

      <div style="background-color: #FFFFFF; width:90%; margin:auto">
        <md-table v-model="searched" md-sort="name" md-sort-order="asc" md-fixed-header>
          <md-table-toolbar>
            <div class="md-toolbar-section-start">
              <h1 class="md-title"> </h1>
            </div>

            <md-field md-clearable class="md-toolbar-section-end">
              <md-input placeholder="Pesquisar por adversário..." v-model="search" @input="searchOnTable" />
            </md-field>
          </md-table-toolbar>

          <md-table-empty-state
            md-label="Sem jogos"
            :md-description="'Não foram encontrados jogos para a sua pesquisa.'">
          </md-table-empty-state>

          <md-table-row slot="md-table-row" slot-scope="{ item }" style="cursor:pointer" @click="verJogo(item.id, item.ativo)">
            <md-table-cell md-label="Competição" md-sort-by="competition">{{ item.competition }}</md-table-cell>
            <md-table-cell md-label="Casa" md-sort-by="casa">{{ item.equipaC }}</md-table-cell>
            <md-table-cell md-label=" " md-sort-by="oddv">{{ item.oddV }}</md-table-cell>
            <md-table-cell md-label="Odds" md-sort-by="odde">{{ item.oddE }}</md-table-cell>
            <md-table-cell md-label=" " md-sort-by="oddd">{{ item.oddD }}</md-table-cell>
            <md-table-cell md-label="Fora" md-sort-by="fora">{{ item.equipaF }}</md-table-cell>
          </md-table-row>
        </md-table>
      </div>
    </div>
  </layout-basic>
</template>


<script> 
import router from "../../router";
import LayoutBasic from '../layouts/Basic.vue'
import axios from 'axios';
const toLower = text => {
  return text.toString().toLowerCase()
}
const searchByName = (items, term) => {
  if (term) {
    return items.filter(item => toLower(item.adv_nome).includes(toLower(term)))
  }
  return items
}

export default {
  name: 'Jogos',
  components: {
      LayoutBasic
  },
  data() {
      return {
          jogos: null,
          search: null,
          searched: [],
      }
  },
  mounted: function() {
    this.checkLoggedIn();
    this.FetchData();
  },
  methods: {
    FetchData: function() {
      var app = this;
      axios.get(process.env.API_URL + "http://localhost:8005/matches/events/" + this.$session.get('user_email') + "/").then(response => {
        this.$session.set('clube', response.data.nome)
        this.$session.set('clubeid', response.data.id)
      });
      axios.get("http://localhost:8005/matches/events/").then(response => {
        app.jogos = response.data
        this.searched = this.jogos
      });
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    verJogo(id, jogo_ativo) {
      this.$session.set('jogoTab', id)
      this.$session.set('activeTab',"jogo")
      if (jogo_ativo){
        this.$session.set('js', 1)
        router.push("/jogo");
      }
      else {
        this.$session.set('js', 0)
        router.push("/stats")
      }
    },

    newUser () {
      window.alert('Noop')
    },

    searchOnTable () {
      this.searched = searchByName(this.jogos, this.search)
    }
  }
}
</script>

<style src="../../../dist/static/css/index.css">


