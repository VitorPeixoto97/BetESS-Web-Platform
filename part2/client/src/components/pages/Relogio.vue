<template>
    <div class="row">
      <h5>{{ this.timer < 1800 ? 1 : 2 }}ª Parte</h5>
      <h5>{{ this.timerMinutes() }} : {{ this.timerSeconds() }}</h5>
    </div>
</template>

<script> 
import router from "../../router";
import axios from 'axios';
export default {
  name: 'Relogio',
  components: {
      LayoutBasic
  },
  data() {
      return {
          timer: 0,
          paused: true,
      }
  },
  mounted: function() {
    //this.checkLoggedIn();
    this.FetchData();
  },
  methods: {
    FetchData: function() {
      
    },
      
    checkLoggedIn() {
      if (!this.$session.has('token')) {
        router.push("/auth");
      }
    },

    timerMinutes: function() {
      time = this.timer;
      if (this.timer > 1800)
        time = this.timer - 1800;
      return Math.floor(time/60);
    },

    timerSeconds: function() {
      time = this.timer;
      if (this.timer > 1800)
        time = this.timer - 1800;
      return time % 60;
    },

    updateClock(){
      console.log(this.convocados)
    }
  },
}
</script>