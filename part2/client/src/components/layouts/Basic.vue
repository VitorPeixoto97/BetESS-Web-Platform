<template>
  <div id="app">

    <slot/>

    <div>
      <div class="phone-viewport">
        <md-bottom-bar md-type="shift" :md-active-item="activeVal">
          <div style="margin: 0 auto; width:100%; background-color:#FF5426;">
            <md-bottom-bar-item id="eventos"   @click="eventos"   md-label="Eventos"       md-icon="explore"></md-bottom-bar-item>
            <md-bottom-bar-item id="apostas"   @click="apostas"   md-label="Apostas"       md-icon="bookmark"></md-bottom-bar-item>
            <md-bottom-bar-item id="notif"     @click="nots"      md-label="Notificações" :md-icon="this.notifs"></md-bottom-bar-item>
            <md-bottom-bar-item id="historico" @click="historico" md-label="Histórico"     md-icon="history"></md-bottom-bar-item>
            <md-bottom-bar-item id="movims"    @click="movims"    md-label="Movimentações" md-icon="credit_card"></md-bottom-bar-item>
            <md-bottom-bar-item id="logout"    @click="logout"    md-label="Sair"          md-icon="power_settings_new"></md-bottom-bar-item>
          </div>
        </md-bottom-bar>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    mounted: function() {
      this.FetchData();
    },
    data() {
      return {
        activeVal: this.$session.get('activeTab'),
        notifs: 'notifications_none'
      }
    },
    methods: {
      logout() {
        if (this.$session.has('token')) {
          this.$session.remove('token');
          this.$router.push("/auth");
        }
      },
      eventos() {
        this.$session.set('activeTab',"eventos")
        this.$router.push('/eventos')
      },
      apostas() {
        this.$session.set('activeTab',"apostas")
        this.$router.push('/apostas')
      },
      movims() {
        this.$session.set('activeTab',"movims")
        this.$router.push('/movimentos')
      },
      historico() {
        this.$session.set('activeTab',"historico")
        this.$router.push('/historico')
      },
      nots() {
        this.$session.set('activeTab',"notif")
        this.$router.push('/notificacoes')
      },
      FetchData(){
        axios.get("http://localhost:8005/betting/notifs/" + this.$session.get('user').id + "/").then(response => {
          console.log(response.data.length);
          if(response.data.length == 0){
            this.notifs='notifications_none'
          }
          else{
            this.notifs='notifications_active'
          }
        });
      }
    }
  }
</script>

<style lang="scss" scoped>
  .phone-viewport {
    position: fixed;
    bottom: 0;
    width: 100%;
    overflow: hidden;
    background: #FFFFFF;
  }
</style>