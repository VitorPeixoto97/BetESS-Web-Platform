<template>
    <div class="container" id="app">    
      <div class="row">
        <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
          <img src="../../assets/hoqueistats.png" alt="HoqueiStats" style="width:70%; display: block;
  margin: auto; padding-top: 30px;">
          <div class="card card-signin my-5">
            <div class="card-body">
              <h5 class="card-title text-center">Entrar</h5>
              <v-form ref="form" class="form-signin" id="login-form" v-model="valid" lazy-validation>
                <div class="form-label-group">
                  <input 
                    type="text"
                    id="inputEmail"
                    ref="email"
                    placeholder="Endereço email"
                    v-model="credentials.username"
                    class="form-control"
                    label="Endereço email"
                    :rules="rules.username"
                    maxlength="70"
                    required
                    autofocus
                  />
                  <label for="inputEmail">Endereço email</label>
                </div>

                <div class="form-label-group">
                  <input 
                    type="password"
                    id="inputPassword"
                    placeholder="Palavra-passe"
                    v-model="credentials.password"
                    class="form-control"
                    label="Palavra-passe"
                    :rules="rules.password"
                    maxlength="20"
                    required
                    autofocus
                  />
                  <label for="inputPassword">Palavra-passe</label>
                </div>

                <button class="btn btn-lg btn-primary btn-block text-uppercase" :disabled="!valid" @click="login">Login</button>
                <div v-if="error==1">
                  <h2 class="card-login-failed text-center">Credenciais incorretas</h2>
                </div>
              </v-form>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import main from '../../main.js';
import axios from 'axios';
import swal from 'sweetalert2';
import router from '../../router';
export default {
    name: 'Auth',
    data: () => ({
        credentials: {},
        valid:true,
        loading:false,
        error:0,
        rules: {
          username: [
            v => !!v || "Um nome de utilizador é necessário.",
            v => (v && v.length > 3) || "Um nome de utilizador deve conter mais do que 3 carateres.",
            v => /^[a-z0-9_]+$/.test(v) || "Um nome de utilizador deve conter apenas letras e dígitos."
          ],
          password: [
            v => !!v || "Uma palavra-passe é necessária.",
            v => (v && v.length > 4) || "Uma palavra-passe deve conter mais do que 4 carateres."
          ]
        }
    }),
    methods: {
        login() {
          // checking if the input is valid
            if (this.$refs.form.validate()) {
              this.loading = true;
              this.error = 0;
              this.$session.set('user_email', this.$refs.email.value);
              axios.post('http://localhost:8000/auth/obtain/', this.credentials).then(res => {
                this.$session.start();
                this.$session.set('token', res.data.token);
                router.push('/jogos');
              }).catch(e => {
                this.loading = false;
                this.error = 1;
                swal({
                  type: 'warning',
                  title: 'Error',
                  text: 'Wrong username or password',
                  showConfirmButton:false,
                  showCloseButton:false,
                  timer:3000
                })
              })
            }
        }
    }
}
</script>

<style src="../../../dist/static/css/login.css">
