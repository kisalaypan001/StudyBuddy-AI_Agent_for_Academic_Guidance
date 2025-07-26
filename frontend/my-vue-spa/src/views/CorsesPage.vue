<template>
      <!-- Sidebar -->
      <div class="sidebar">
        <a href="#" class="selected-icon"><img src="@/Images/Icon-01_selected.svg" alt="Icon 1"></a>
        <a href="#"><img src="@/Images/Icon-02.svg" alt="Icon 2"></a>
        <a href="#"><img src="@/Images/Icon-03.svg" alt="Icon 3"></a>
        <a href="#"><img src="@/Images/Icon-04.svg" alt="Icon 4"></a>
        <a href="#"><img src="@/Images/Icon-05.svg" alt="Icon 5"></a>
        <a href="#"><img src="@/Images/Icon-06.svg" alt="Icon 6"></a>
        <a href="#"><img src="@/Images/Icon-07.svg" alt="Icon 7"></a>
        <a href="#"><img src="@/Images/Icon-08.svg" alt="Icon 8"></a>
        <a href="#"><img src="@/Images/Icon-09.svg" alt="Icon 9"></a>
        <a href="#"><img src="@/Images/Icon-10.svg" alt="Icon 10"></a>
        <a href="#"><img src="@/Images/Icon-11.svg" alt="Icon 11"></a>
    </div>
  
      <!-- Content -->
      <div class="content">
        <h1>My current courses</h1>
        <div class="course-card">
          <h2>Programming in Python</h2>
          <p>Course Description</p>
          <router-link to="/python" class="course-link">Go to Course</router-link>
        </div>
        <div class="course-card">
          <h2>English 2</h2>
          <p>Course Description</p>
          <router-link to="/english" class="course-link">Go to Course</router-link>
        </div>
      </div>
  
      <!-- Footer -->
      <div class="footer">
        <p>&copy; 2025 StudyBuddy AI Assistant. All rights reserved.</p>
      </div>
  </template>
  
  <script>
  export default {
    name: 'CoursesPage',
    methods: {
      logout() {
        // Add logout functionality here, e.g., clear user session or navigate to login page
        console.log('User logged out');
      }
    }
  }
  </script>
  <style scoped>
  /* General Styles */
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
  }
  </style>