<template>
  <div>
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="#"><img src="@/Images/Icon-01.svg" alt="Icon 1"></a>
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

    <!-- Main Content -->
    <div class="main-content_1">
      <div class="content-wrapper">
        <!-- Student Details Section -->
        <div class="content-box">
          <h2>Student Details</h2>
          <div class="search-container">
            <input type="text" placeholder="Search students by roll number or name..." v-model="searchQuery"
              class="search-input" @input="handleSearch" />
          </div>
          <div class="student-list">
            <div v-if="filteredStudents.length > 0">
              <div class="student-card" v-for="student in filteredStudents" :key="student.id">
                <span class="roll-number">Roll No: {{ student.rollNo }}</span>
                <button class="view-btn" @click="openModal(student)">View</button>
              </div>
            </div>
            <div v-else class="no-results">
              No students found matching "{{ searchQuery }}"
            </div>
          </div>

          <button class="generate-report-btn" @click="generateReport">Generate Report 🤖</button>
        </div>

        <!-- Report Visualization Section -->
        <div class="content-box visualization-box">
          <template v-if="!showPdfViewer">
            <h2>Report Visualisation</h2>
            <div class="initial-image-container">
              <img src="@/Images/illustration-of-colorful-bar-graph-with-six-step-vector.jpg"
                alt="Initial Visualization" class="visualization-image" />
            </div>
            <p class="generate-instruction">Click the Generate Report button to Visualize Data</p>
          </template>
          <div v-else class="pdf-container">
            <iframe v-if="showPdfViewer" :src="pdfUrl" class="pdf-viewer" type="application/pdf" />
          </div>
        </div>

        <!-- Text Report Section -->
        <div class="content-box">
          <h2>Text Report</h2>
          <div class="text-report-content">
            <div v-if="!showTextSummary && !showAIResponse">
              <p>Click the Generate Report button to get a Textual Summary of Data</p>
            </div>
            <div v-else-if="showTextSummary" class="text-summary">
              {{ generatedSummary }}
            </div>
            <div v-else class="ai-response">
              Relevant Reply from AI Bot appears here
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Student Details Modal -->
    <div v-if="selectedStudent" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeModal">&times;</button>
        <h3>Student Details</h3>
        <div class="student-info">
          <div class="info-row">
            <span class="label">Name:</span>
            <span class="value">{{ selectedStudent.name }}</span>
          </div>
          <div class="info-row">
            <span class="label">Roll Number:</span>
            <span class="value">{{ selectedStudent.rollNo }}</span>
          </div>
          <div class="info-row">
            <span class="label">Email:</span>
            <span class="value">{{ selectedStudent.email }}</span>
          </div>
        </div>

        <div class="marks-info" v-if="selectedStudent.marks.length > 0">
          <h4>Marks:</h4>
          <table style="width:100%; margin-top: 10px;">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Quiz 1</th>
                <th>Quiz 2</th>
                <th>End Term</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(mark, index) in selectedStudent.marks" :key="index">
                <td>{{ mark.subject }}</td>
                <td>{{ mark.quiz_1 }}</td>
                <td>{{ mark.quiz_2 }}</td>
                <td>{{ mark.end_term }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else style="margin-top: 10px;">No marks available.</div>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>&copy; 2025 StudyBuddy AI Assistant. All rights reserved.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      showAIResponse: false,
      showTextSummary: false,
      showPdfViewer: false,
      selectedStudent: null,
      students: [],
      generatedSummary: '',
      pdfUrl: ''  // Add this in your data() return block
      // <--- NEW
    };
  }
  ,
  mounted() {
    this.fetchStudents();
  },
  computed: {
    filteredStudents() {
      const query = this.searchQuery.toLowerCase().trim();
      return query
        ? this.students.filter(
          student =>
            student.rollNo.toLowerCase().includes(query) ||
            student.name.toLowerCase().includes(query)
        )
        : this.students;
    }
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await fetch('http://localhost:5000/api/students/all');
        const data = await response.json();
        this.students = data;
      } catch (err) {
        console.error('Failed to fetch students:', err);
      }
    },
    generateReport() {
      fetch('http://localhost:5000/api/generate-reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject: '' })
      })
        .then(res => res.json())
        .then(data => {
          if (data.response && data.response.pdf_ready) {
            this.generatedSummary = data.response.summary;
            this.showTextSummary = true;
            this.showAIResponse = false;

            // Only fetch PDF once it's confirmed to be ready
            this.fetchPdfAfterDelay();
          }
        })
        .catch(err => {
          console.error("Error generating report:", err);
        });
    },
    fetchPdfAfterDelay() {
      setTimeout(() => {
        fetch('http://localhost:5000/api/get-report-pdf')
          .then(res => res.blob())
          .then(blob => {
            const blobUrl = URL.createObjectURL(blob);
            this.$nextTick(() => {
              this.pdfUrl = blobUrl;
              this.showPdfViewer = true;
            });
          })
          .catch(err => {
            console.error("Error fetching PDF:", err);
          });
      }, 3000);
    }



    ,
    openModal(student) {
      this.selectedStudent = student;
      document.body.style.overflow = 'hidden';
    },
    closeModal() {
      this.selectedStudent = null;
      document.body.style.overflow = 'auto';
    }
  }
};
</script>


<style scoped>
.content-wrapper {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
}

.content-box {
  flex: 1 1 0;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 465px;
  display: flex;
  flex-direction: column;
  width: 33.333%;
  min-width: 0;
}

.visualization-box {
  position: relative;
}

.initial-image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  height: calc(100% - 80px);
}

.visualization-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.pdf-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: white;
  border-radius: 8px;
}

.pdf-viewer {
  width: 100%;
  height: 100%;
  border: none;
}

.generate-instruction {
  text-align: center;
  color: #666;
  margin-top: 10px;
  font-size: 14px;
}

.search-container {
  margin-bottom: 15px;
  width: 100%;
}

.search-input {
  width: 95%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
}

.student-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
}

.student-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 8px;
  transition: background-color 0.2s ease;
}

.student-card:hover {
  background: #e9ecef;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #6c757d;
  font-style: italic;
}

.roll-number {
  font-size: 0.9rem;
  color: #333;
}

.view-btn {
  padding: 4px 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.view-btn:hover {
  background: #0056b3;
}

.generate-report-btn {
  width: 100%;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: auto;
  font-size: 14px;
  transition: background-color 0.2s ease;
}

.generate-report-btn:hover {
  background: #218838;
}

.text-report-content {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 15px;
}

.text-summary {
  text-align: justify;
  margin: 20px 0;
  color: #666;
}

.ai-response {
  text-align: center;
  padding: 20px;
  color: #333;
  font-size: 16px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.student-info {
  margin-top: 20px;
}

.info-row {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  width: 120px;
  color: #666;
}

.value {
  flex: 1;
  color: #333;
}

h3 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}
</style>