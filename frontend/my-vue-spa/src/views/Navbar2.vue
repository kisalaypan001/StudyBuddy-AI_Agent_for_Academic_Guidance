<template>
    <nav class="navbar">
      <a class="navbar-brand" href="#">
        <img src="@/Images/logo.jpg" alt="IIT Madras BS Degree Program">
      </a>
      <div class="navbar-right">
        <router-link to="/" class="button">SIGN OUT</router-link>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "SimpleNavbar",
  };
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,.1);
  }
  
  .navbar-brand {
    text-decoration: none;
  }
  
  .navbar-brand img {
    height: 40px;
    width: auto;
  }
  
  .navbar-right {
    margin-left: auto;
    padding-right: 1rem;
  }
  
  .button {
    text-decoration: none;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    background-color: #dc3545;
    color: white;
    font-weight: bold;
    font-size: 0.9rem;
  }
  
  .button:hover {
    background-color: #c82333;
  }
  </style>