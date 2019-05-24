<template>
  <div id="app">

    <slot/>

    <div>
      <div class="phone-viewport">
        <md-bottom-bar md-type="shift" :md-active-item="activeVal">
          <div style="margin: 0 auto; width: 100%;">
            <md-bottom-bar-item id="jogos" @click="jogos" md-label="Jogos" md-icon="menu"></md-bottom-bar-item>
            <md-bottom-bar-item id="jogo" @click="jogo" md-label="Jogo" md-icon="home"></md-bottom-bar-item>
            <md-bottom-bar-item id="settings" md-label="Definições" md-icon="settings"></md-bottom-bar-item>
            <md-bottom-bar-item id="logout" @click="logout" md-label="Logout" md-icon="power_settings_new"></md-bottom-bar-item>
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
      jogo() {
        this.$session.set('activeTab',"jogo")
        this.$router.push('/jogo')
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