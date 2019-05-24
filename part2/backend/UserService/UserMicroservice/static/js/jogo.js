import axios from 'axios';

new Vue({
    el: '#starting',
    delimiters: ['${','}'],
    data: {
        jogos: [],
        loading: false,
        currentJogo: {},
        message: null,
        newJogo: { 'tipo': null, 'formacao': 0, 'adversario': 0, 'casa': false, 'data': null, 'hora': null, 'grelhaCampo': "0x0", 'grelhaBaliza': "0x0"},
    },
    mounted: function() {
        this.getJogos();
    },
    methods: {
        getJogos: function() {
            this.loading = true;
            axios.get('/get_jogos/1')
            .then((response) => {
                this.jogos = response.data;
                this.loading = false;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
    },
});
