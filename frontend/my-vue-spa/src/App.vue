<template>
  <div id="app">
    <!-- Conditionally render different navbars based on current route -->
    <Navbar v-if="!isDashboardRoute" />
    <Navbar2 v-if="isDashboardRoute" />
    
    <!-- Router view to display different pages -->
    <router-view />
  </div>
</template>

<script>
import Navbar from './views/Navbar.vue';
import Navbar2 from './views/Navbar2.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    Navbar2
  },
  computed: {
    isDashboardRoute() {
      // Check if current route is a dashboard route
      const dashboardRoutes = ['/student-dashboard', '/instructor-dashboard','/python','/english','/coursespage','/coding','/python-grades','/english-grades'];
      return dashboardRoutes.includes(this.$route.path);
    }
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>