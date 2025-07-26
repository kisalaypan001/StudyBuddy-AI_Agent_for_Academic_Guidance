<template>
    <div class="main-container">
      <!-- Left White Container -->
      <div class="left-container">
        <h2>Sign-Up</h2>
        <p>Create an account by providing your details below.</p>
        <form @submit.prevent="handleSubmit">
          <label for="name">Full Name</label>
          <input
            type="text"
            id="name"
            v-model="name"
            placeholder="Enter your full name"
            required
          />
  
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
          />
  
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
  
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm your password"
            required
          />
  
          <button type="submit">Sign Up</button>
        </form>
  
        <router-link to="/loginpage" class="sign-up-link">Already have an account? Log in here</router-link>
      </div>
  
      <!-- Right Announcements Section -->
      <div class="right-container">
        <h2>Latest Updates / Announcements</h2>
  
        <div class="announcement">
          <span>Quiz Dates for Jan 2025 Term</span>
          <p>Quiz 1: 23 Feb 2025<br />Quiz 2: 16 Mar 2025<br />End Term: 13 Apr 2025</p>
        </div>
  
        <div class="announcement">
          <span>Announcement for Jan 2025 Term Course Registration Form</span>
          <p>January 2025 Term Course Registration Form is now open.<br />Deadline: 3rd January 2025</p>
        </div>
  
        <div class="announcement">
          <span>Important Announcement for Course Registration</span>
          <p>https://docs.google.com/document/d/e/2PACX-1vS_...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SignUpPage', // Name of the component
    data() {
      return {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
      };
    },
    methods: {
      handleSubmit() {
        // Handle form submission logic (e.g., API request to create a new user)
        if (this.password !== this.confirmPassword) {
          alert("Passwords do not match!");
          return;
        }
  
        console.log('Form submitted', { name: this.name, email: this.email, password: this.password });
  
        // You would typically send the data to the backend for registration
        // Example: this.$axios.post('/api/signup', { name, email, password })
  
        // For demonstration, navigate to the login page after successful signup
        this.$router.push({ name: 'LoginPage' }); // Navigates to the login page
      }
    },
  };
  </script>
  
  