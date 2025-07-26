<template>
    <!-- Navbar Template -->
    <nav class="navbar">
      <a class="navbar-brand" href="#">
        <img src="@/Images/logo.jpg" alt="IIT Madras BS Degree Program">
      </a>
      <button class="navbar-toggler" aria-label="Toggle navigation" @click="toggleNavbar">
        <i class="fas fa-bars"></i>
      </button>
      <ul class="navbar-nav" :class="{'active': isActive}">
        <li class="nav-item dropdown">
          <a class="nav-link" href="#">Academics <i class="fas fa-angle-down"></i></a>
          <ul class="dropdown-menu">
              <a class="dropdown-item" href="#">Overall Structure</a>
              <a class="dropdown-item" href="#">Term Structure</a>
              <a class="dropdown-item" href="#">Course Registrations</a>
              <a class="dropdown-item" href="#">Assessments</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Exam Cities</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Fee Structure</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Foundation Level</a>
              <a class="dropdown-item" href="#">Diploma Level</a>
              <a class="dropdown-item" href="#">BSc Degree Level</a>
              <a class="dropdown-item" href="#">BS Degree Level</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Sample Certificates</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Academic Calendar</a>
          </ul>
        </li>
        <li class="nav-item dropdown">
        <a class="nav-link"> Admissions<i class="fas fa-angle-down"></i></a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">Important Dates</a>
          <a class="dropdown-item" href="#">Mandatory Requirements</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Eligibility to Apply</a>
          <a class="dropdown-item" href="#">Application Process</a>
          <a class="dropdown-item" href="#">Admission to the Foundation Level</a>
          <a class="dropdown-item" href="#">1. Regular Entry</a>
          <a class="dropdown-item" href="#">2. JEE-based Entry</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">International Students</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link" href="#">Resources <i class="fas fa-angle-down"></i></a>
        <div class="dropdown-menu" >
          <a class="dropdown-item" href="#">Help Videos</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">In the Media</a>
          <a class="dropdown-item" href="#">Archive</a>
        </div>
      </li>
      <li class="dropdown nav-item ">
        <a class="nav-link">
          Student Life
          <i class="fas fa-angle-down"></i>
        </a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">Student Houses & Societies</a>
          <a class="dropdown-item" href="#" target="_blank">PARADOX / Student Festivals</a>
        </div>
      </li>
      <li class="nav-item ">
        <a class="nav-link">
          School Connect
        </a>
      </li>
      <li class="dropdown nav-item ">
        <a class="nav-link">
          Achievements
          <i class="fas fa-angle-down"></i>
        </a>
        <div class="dropdown-menu"  >
          <div class="dropdown-item">Recognition</div>
          <a class="dropdown-item" style="padding-left: 30px;" href="#" target="_blank">1. Toppers Page</a>
          <a class="dropdown-item" style="padding-left: 30px;" href="#" target="_blank">2. Student's Best Projects</a>
          <a class="dropdown-item" style="padding-left: 30px;" href="#" target="_blank">3. Teaching Assistance</a>
          <a class="dropdown-item" style="padding-left: 30px;" href="#" target="_blank">4. Alumni</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Testimonials</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#" target="_blank">Research and Publication</a>
        </div>
      </li>
      <li class="nav-item ">
        <a class="nav-link">
          Events
        </a>
      </li>

      <li class="nav-item ">
        <a class="nav-link">
          FAQ
        </a>
      </li>
      <li class="dropdown nav-item ">
        <a class="nav-link">
          About IITM
          <i class="fas fa-angle-down"></i>
        </a>
        <div class="dropdown-menu" aria-labelledby="navbar-default_dropdown_1">
          <a class="dropdown-item" href="https://study.iitm.ac.in/ds/aboutIITM.html">About IIT Madras</a>
          <a class="dropdown-item" href="https://study.iitm.ac.in/ds/aboutIITM.html#FC">Faculty Co-ordinators</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="https://study.iitm.ac.in/ds/aboutIITM.html#footer">Contact Us</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" target="_blank" href="https://podgoodies.iitmadrasonline.in/">Merchandise</a>
        </div>
      </li>
      
      <li class="nav-item ">
        <a class="nav-link" >
          Partnerships
        </a>
      </li>

      <li class="nav-item ">
        <a class="nav-link" >
          Placements
        </a>
      </li>
      <li class="nav-item ">
        <router-link to="/loginpage" class="button">SIGN IN</router-link>
      </li>
    </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: "AppNavbar", // Change component name to multi-word
    data() {
      return {
        isActive: false,
      };
    },
    methods: {
      toggleNavbar() {
        this.isActive = !this.isActive;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Insert your styles from the original code */
  </style>
  