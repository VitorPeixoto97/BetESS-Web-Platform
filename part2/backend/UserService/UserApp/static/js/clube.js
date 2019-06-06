new Vue({
    el: '#starting',
    delimiters: ['${','}'],
    data: {
        clubes: [],
        loading: false,
        currentClube: {},
        message: null,
        newClube: { 'nome': null, 'cor': null, 'simbolo': null },
    },
    mounted: function() {
        this.getClubes();
    },
    methods: {
        getClubes: function() {
            this.loading = true;
            this.$http.get('/rest/clube/')
            .then((response) => {
                this.clubes = response.data;
                this.loading = false;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
        getClube: function(id) {
            this.loading = true;
            this.$http.get('/rest/clube/${id}/')
              .then((response) => {
                this.currentClube = response.data;
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        addClube: function() {
            this.loading = true;
            this.$http.post('/api/clube/', this.newClube)
              .then((response) => {
                this.loading = false;
                this.getClubes();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        updateClube: function() {
            this.loading = true;
            this.$http.put('/api/clube/${this.currentClube.clube_id}/', this.currentClube)
              .then((response) => {
                this.loading = false;
                this.currentClube = response.data;
                this.getClubes();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        deleteClube: function(id) {
            this.loading = true;
            this.$http.delete('/api/clube/${id}/' )
              .then((response) => {
                this.loading = false;
                this.getClubes();
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
    },
});