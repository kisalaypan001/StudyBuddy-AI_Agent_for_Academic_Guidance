const { createApp } = Vue;

createApp({
    data() {
        return {
            message: 'Hello, Vue.js SPA!',
            currentView: 'home', // Default page
        };
    },
    methods: {
        changeMessage() {
            this.message = 'You clicked the button!';
        }
    }
}).mount('#app');
