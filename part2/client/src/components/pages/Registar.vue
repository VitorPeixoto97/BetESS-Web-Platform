<template>
    <div class="container" id="app">    
      <div class="row">
        <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
          <img src="../../assets/logo.png" alt="BetESS" style="width:90%; display: block;
  margin: auto; padding-top: 30px;">
          <div class="card card-signin my-5">
            <div class="card-body">
              <h5 class="card-title text-center">Registar</h5>
              <v-form ref="form" class="form-signin" lazy-validation>
                <div class="form-label-group">
                  <input 
                    type="text"
                    id="inputEmail"
                    ref="email"
                    placeholder="Endereço email"
                    v-model="credentials.username"
                    class="form-control"
                    label="Endereço email"
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
                    required
                    autofocus
                  />
                  <label for="inputPassword">Palavra-passe</label>
                </div>

                <div class="form-label-group">
                  <input 
                    type="text"
                    id="inputName"
                    placeholder="Nome"
                    v-model="credentials.name"
                    class="form-control"
                    label="Nome"
                    required
                    autofocus
                  />
                  <label for="inputName">Nome</label>
                </div>
                
                <div class="row" style="margin-bottom:12px; margin-left:0px;">
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountminus()">‒</button>
                  <input id="inputCoins" ref="valor" v-model="credentials.coins" class="amount" label="Valor da aposta"/>
                  <button class="btn btn-lg text-uppercase btn-minusplus" @click="amountplus()">+</button>
                  <label class="label-coins" for="inputCoins">Saldo inicial (5€ Oferta!)</label>
                </div>

                <div style="margin-bottom:12px; margin-top:20px;">
                  <b-form-checkbox id="inputPremium" v-model="credentials.premium" switch>
                    <label class="label-coins" style="margin:auto">Aderir ao pacote Premium.
                      <a @click="premium()" style="cursor: pointer; color:#FF5426"> Ver vantagens</a>
                    </label>
                  </b-form-checkbox>
                </div>

                <div style="margin-bottom:30px; margin-top:20px;">
                  <b-form-checkbox id="inputAuth" v-model="credentials.authorization" switch>
                    <label class="label-coins" style="margin:auto">Aceito os termos e condições.
                    <a @click="termscond()" style="cursor: pointer; color:#FF5426"> Ler</a>
                    </label>
                  </b-form-checkbox>
                </div>
                
                <button class="btn btn-lg btn-primary btn-block text-uppercase" @click="submit">Registar</button>
                <h6 class="text-center" style=" margin-top:20px;"><a @click="back()" style="cursor: pointer; color:#FF5426">Voltar</a></h6>
              </v-form>
            </div>
          </div>
        </div>
      </div>

      <div class="row main-row" v-if="this.readPremium">
        <div class="column full-column">
          <v-container>
          <v-card color="white" class="my-card event">
              <p primary-title class="user-name"><b>Vantagens de ser Premium</b></p>
              <p class="text">Ao aderir ao pacote Premium da nossa casa de apostas online, tem acesso a eventos exclusivos. Os eventos exclusivos para utilizadores Premium estão cotados com odds mais altas para aumentar o seu retorno!</p>
              <p class="text">Para aderir basta marcar a checkbox no momento do seu registo! Boa sorte!</p>
              <p class="text">A subscrição Premium está sujeita a um débito mensal de 3€ efetuado automaticamente na sua conta bancária.</p>
          </v-card>
          </v-container>
        </div>
      </div>

      <div class="row main-row" v-if="this.readTerms">
        <div class="column full-column">
          <v-container>
          <v-card color="white" class="my-card event" style="height:250px;">
              <p primary-title class="user-name"><b>Termos e condiçõs</b></p>
              <p class="text">1. Ao aderir a este serviço está a dar consentimento para efetuar transações bancárias automaticamente na sua conta. Estas transações serão apenas acionadas por si, excecionalmente para utilizadores Premium na qual a aplicação efetua um débito mensal de 3€ automaticamente.</p>
              <p class="text">2. Os seus dados são apenas para uso interno estatístico e não serão divulgados a entidades exteriores.</p>
              <p class="text">3. Jogos de azar podem desenvolver-se em vícios. Por favor, jogue com moderação.</p>
          </v-card>
          </v-container>
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
        credentials: {
          username: '',
          password: '',
          name: '',
          coins: 5,
          premium: false,
          authorization: false
        },
        readTerms: false,
        readPremium: false,
        error: ''
    }),
    methods: {
      submit() {
        if (this.validate()) {
          if(this.credentials.authorization){
            axios.post('http://localhost:8005/register/', JSON.stringify(this.credentials)).then(res => {
              this.$notify({
                group: 'foo',
                type: 'success',
                title: 'Sucesso',
                text: 'Registo efetuado com sucesso.'
              });
              router.push('/auth');
            }).catch(e => {
              this.$notify({
                group: 'foo',
                type: 'error',
                title: 'Erro',
                text: e.response.data
              });
            })
          }
          else{
            this.$notify({
              group: 'foo',
              type: 'error',
              title: 'Aviso',
              text: 'Necessita de aceitar os termos e condições para se registar na BetESS.'
            });
          }
        }
        else{
          this.$notify({
            group: 'foo',
            type: 'error',
            title: 'Aviso',
            text: this.error
          });
        }
      },
      back(){
        router.push('/auth')
      },
      amountminus(){
        if(this.credentials.coins>5)
          this.credentials.coins = this.credentials.coins-1
      },
      amountplus(){
        if(this.credentials.coins<100)
          this.credentials.coins = this.credentials.coins+1
      },
      premium(){
        if(this.readPremium)
          this.readPremium=false;
        else 
          this.readPremium=true;
      },
      termscond(){
        this.readTerms=true;
      },
      validate(){
        if(this.credentials.username.length<6){
          this.error='Endereço email deve ter mais do que 6 carateres.';
          return false;
        }
        else if(this.credentials.password.length<6){
          this.error='Palavra-passe deve ter mais do que 6 carateres.';
          return false;
        }
        else if(this.credentials.name.length<3){
          this.error='Nome deve ter mais do que 3 carateres.';
          return false;
        }
        
        
        else return true;
      }
    }
}
</script>

<style src="../../../dist/static/css/login.css">
