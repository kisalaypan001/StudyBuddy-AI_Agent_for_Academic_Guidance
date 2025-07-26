<template>
  <!-- Main Container -->
  <div class="main-container-python">
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="/python"><img src="@/Images/sidebar-modules.svg" alt="Modules"></a>
      <a href="#" class="selected-icon"><img src="@/Images/sidebar-grades-selected.svg" alt="Grades"></a>
    </div>
    
    <!-- Sidebar for Modules -->
    <div class="sidebar-grades">
      <h2>Grades</h2>
      <ul>
        <li class="grade-item" v-for="(week, index) in 12" :key="index">
          <span>Week {{ index + 1 }}</span>
          <span class="grade">{{ grades[index] }}/100</span>
        </li>
        <li class="grade-item">
          <span>Quiz 1</span>
          <span class="grade">{{ grades[12] }}/100</span>
        </li>
        <li class="grade-item">
          <span>Quiz 2</span>
          <span class="grade">{{ grades[13] }}/100</span>
        </li>
        <li class="grade-item">
          <span>OPPE 1</span>
          <span class="grade">{{ grades[14] }}/100</span>
        </li>
        <li class="grade-item">
          <span>OPPE 2</span>
          <span class="grade">{{ grades[15] }}/100</span>
        </li>
        <li class="grade-item">
          <span>End Term</span>
          <span class="grade">{{ grades[16] }}/100</span>
        </li>
      </ul>
    </div>
    
    <!-- Content Section -->
    <div class="content-grades">
      <h1>Grades Overview</h1>
      <p>Here you can track your progress and view your assignment and exam scores.</p>
      
      <div class="grade-summary">
        <h3>Overall Performance</h3>
        <p>Average Grade: <strong>{{ averageGrade }}%</strong></p>
        <progress :value="averageGrade" max="100"></progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      grades: [
        85, 88, 90, 87, 92, 85, 89, 93, 91, 86, 88, 90, // Weeks 1-12
        95, 94, // Quiz 1, Quiz 2
        92, 90, // OPPE 1, OPPE 2
        89 // End Term
      ],
    };
  },
  computed: {
    averageGrade() {
      return (this.grades.reduce((a, b) => a + b, 0) / this.grades.length).toFixed(2);
    }
  }
};
</script>
