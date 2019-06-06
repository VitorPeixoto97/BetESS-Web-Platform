new Vue({
    el: '#starting',
    delimiters: ['${','}'],
    data: {
        atletas: []
        inicial: [],
        loading: false,
        message: null,
    },
    mounted: function() {
        this.getAtletas();
    },
    methods: {
        getAtletas: function() {
            this.loading = true;
            this.$http.get('/rest/atleta/')
            .then((response) => {
                this.atletas = response.data;
                this.loading = false;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
        toggleAtleta: function(id) {
            if(inicial.contains(id)){
              inicial.filter(id)
            }
            else{
              inicial.push(id)
            }
        },
        addInicial: function() {
            this.loading = true;
            inicial.forEach(this.$http.post('/rest/atleta/', this.newAtleta)
              .then((response) => {
                this.loading = false;
                this.getAtletas();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              }))
        },
    }
});