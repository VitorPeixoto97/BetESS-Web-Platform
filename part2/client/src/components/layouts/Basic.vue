<template>
  <div id="app">

    <slot/>

    <div>
      <div class="phone-viewport">
        <md-bottom-bar md-type="shift" :md-active-item="activeVal">
          <div style="margin: 0 auto; width:100%; background-color:#FF5426;">
            <md-bottom-bar-item id="jogos"     @click="jogos"   md-label="Eventos"       md-icon="explore"></md-bottom-bar-item>
            <md-bottom-bar-item id="apostas"   @click="apostas" md-label="Apostas"       md-icon="bookmark"></md-bottom-bar-item>
            <md-bottom-bar-item id="notifs"                     md-label="Notificações"  md-icon="notifications"></md-bottom-bar-item>
            <md-bottom-bar-item id="historico" @click=""        md-label="Histórico"     md-icon="history"></md-bottom-bar-item>
            <md-bottom-bar-item id="cash"                       md-label="Movimentações" md-icon="credit_card"></md-bottom-bar-item>
            <md-bottom-bar-item id="logout"    @click="logout"  md-label="Sair"          md-icon="power_settings_new"></md-bottom-bar-item>
          </div>
        </md-bottom-bar>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        activeVal: this.$session.get('activeTab')
      }
    },
    methods: {
      logout() {
        if (this.$session.has('token')) {
          this.$session.remove('token');
          this.$router.push("/auth");
        }
      },
      jogos() {
        this.$session.set('activeTab',"jogos")
        this.$router.push('/jogos')
      },
      apostas() {
        this.$session.set('activeTab',"apostas")
        //this.$router.push('/apostas')
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