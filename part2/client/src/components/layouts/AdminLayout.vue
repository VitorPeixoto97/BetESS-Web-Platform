<template>
  <div id="app">

    <slot/>

    <div>
      <div class="phone-viewport">
        <md-bottom-bar md-type="shift" :md-active-item="activeVal">
          <div style="margin: 0 auto; width:100%; background-color:#FF5426;">
            <md-bottom-bar-item id="eventos"      @click="eventos"      md-label="Eventos"       md-icon="explore"></md-bottom-bar-item>
            <md-bottom-bar-item id="equipas"      @click="equipas"      md-label="Equipas"       md-icon="people"></md-bottom-bar-item>
            <md-bottom-bar-item id="historico"    @click="historico"    md-label="Histórico"     md-icon="history"></md-bottom-bar-item>
            <md-bottom-bar-item id="logout"       @click="logout"       md-label="Sair"          md-icon="power_settings_new"></md-bottom-bar-item>
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
      eventos() {
        this.$session.set('activeTab',"eventos")
        this.$router.push('/admineventos')
      },
      equipas() {
        this.$session.set('activeTab',"equipas")
        this.$router.push('/adminequipas')
      },
      historico() {
        this.$session.set('activeTab',"historico")
        this.$router.push('/adminhistorico')
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