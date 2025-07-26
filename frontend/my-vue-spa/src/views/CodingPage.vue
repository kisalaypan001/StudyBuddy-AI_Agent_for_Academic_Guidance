<template>
  <div class="main-container-python">
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="/python" class="selected-icon"><img src="@/Images/sidebar-modules-selected.svg" alt="Icon 1"></a>
      <a href="python-grades"><img src="@/Images/sidebar-grades.svg" alt="Icon 2"></a>
    </div>

    <div class="sidebar-python">
      <h2>Modules</h2>
      <ul>
        <li class="module"><span>Course Introduction</span></li>
        <li class="module"><span>Course Project</span></li>
        <li class="module">
          <span>Week 1</span>
          <ul class="sub-modules">
            <li class="sub-module">
              <router-link to="/python" class="module">
                <span>1.1 Introduction to Replit</span>
                <span class="tag">Video</span>
              </router-link>
            </li>
            <li class="sub-module"><span>1.2 More on Replit, print and Common Mistakes</span><span class="tag">Video</span></li>
            <li class="sub-module active"><span>PA1.2: Programming Assignment 1.2 - Not Graded</span><span class="tag">Assignment</span></li>
            <li class="sub-module"><span>1.3 A Quick Introduction to Variables</span><span class="tag">Video</span></li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Content Area -->
    <div class="content-python">
      <div class="video-details">
        <h1>Practice Programming Assignment 1.1:</h1>
        <p>Topic: Introduction to Replit</p>
        <div class="rating">
          <span>★★★★★  - / 5 (0 reviews)</span> | 
          <a href="#" style="color: #007acc;">Submit a review</a>
        </div>
      </div>

      <div class="programming-challenge">
        <h2>Programming Challenge</h2>
        <p>Write a Python program to print the first 5 positive integers in ascending order.</p>
        <textarea v-model="userCode" placeholder="Enter your Python code here..."></textarea>
        <button @click="runCode">Run Code</button>

        <h3>Expected Output:</h3>
        <div id="expected-output">1 2 3 4 5</div>

        <h3>Actual Output:</h3>
        <div id="actual-output">{{ actualOutput }}</div>

        <h3>Result:</h3>
        <p id="result" :style="{ color: resultColor }">{{ resultMessage }}</p>
      </div>
    </div>

    <!-- Right Panel -->
    <div class="right-panel">
      <img 
        src="@/Images/prog-assistant.png" 
        alt="AI Assistant" 
        width="150px" 
        @click="togglePeerRecommendations" 
        class="peer-group-img" 
      />

      <div class="prog-assistant-container" v-if="showPeerRecommendations">
        <h2>Programming Assistant</h2>
        <ul>
          <li v-for="(message, index) in assistantResponses" :key="index" v-html="formatMessage(message)">
            
          </li>
</ul>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userCode: "",
      actualOutput: "",
      resultMessage: "",
      resultColor: "black",
      showPeerRecommendations: false,
      assistantResponses: [],
    };
  },
  methods: {
    runCode() {
      const correctOutput = "1\n2\n3\n4\n5\n"; // Expected output

      let isCorrect = this.userCode.includes("print") &&
                      this.userCode.includes("for") &&
                      this.userCode.includes("range(1, 6)");

      // Simulated mock output (actual execution would be handled on backend)
      let mockOutput = isCorrect ? "1\n2\n3\n4\n5\n" : "SyntaxError: invalid syntax";

      this.actualOutput = mockOutput;

      if (isCorrect) {
        this.resultMessage = "Correct! Your output matches the expected output.";
        this.resultColor = "green";
      } else {
        this.resultMessage = "Incorrect. Please try again.";
        this.resultColor = "red";
      }
    },

    togglePeerRecommendations() {
      this.showPeerRecommendations = !this.showPeerRecommendations;
      if (this.showPeerRecommendations) {
        this.getCodeAssistResponse();
      }
    },

    async getCodeAssistResponse() { 
  try {
    console.log("Sending request to backend...");

    // Validate user input before sending request
    if (!this.userCode.trim()) {
      this.assistantResponses = ["Please enter some code before requesting assistance."];
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/codeassist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problem_statement: "Write a Python program to print the first 5 positive integers in ascending order.",
        error_code: this.userCode.trim() // Taking input dynamically from the textarea
      })
    });

    console.log("Response received:", response);

    if (!response.ok) {
      throw new Error(`Server error: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Parsed data:", data);

    if (data && data.response) {
      // Clean up response formatting
      let formattedResponse = data.response
        .replace(/={3,}/g, "")  // Remove long === lines
        .replace(/-{3,}/g, "")  // Remove long --- lines
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Convert **bold** to <strong>
        .replace(/### (.+)/g, "<h3>$1</h3>") // Convert ### headers
        .replace(/#### (.+)/g, "<h4>$1</h4>") // Convert #### subheaders
        .replace(/\* (.+)/g, "<li>$1</li>") // Convert bullet points
        .replace(/\n\s+/g, "\n") // Remove unnecessary spaces
        .replace(/\n/g, "<br>") // Convert new lines to HTML breaks
        .trim();

      this.assistantResponses = formattedResponse.split("<br>").filter(msg => msg.trim() !== "");
    } else {
      this.assistantResponses = ["No meaningful response received from the assistant."];
    }
  } catch (error) {
    console.error("Error fetching assistant response:", error);
    this.assistantResponses = ["Failed to get response. Please try again."];
  }
},

formatMessage(message) {
  return message
    .replace(/\n/g, "<br>") // Convert new lines to HTML breaks
    .replace(/### (.+)/g, "<h3>$1</h3>") // Convert ### headers
    .replace(/#### (.+)/g, "<h4>$1</h4>") // Convert #### subheaders
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>") // Convert bold text
    .replace(/\* (.+)/g, "<li>$1</li>") // Convert bullet points
    .replace(/---/g, "<hr>"); // Convert horizontal lines
}
  }
};
</script>

<style scoped>
/* Base styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.prog-assistant-container {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  max-width: 90%;
  font-family: Arial, sans-serif;
}

.prog-assistant-container h2 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #007acc;
}
.prog-assistant-container li {
  background: #ffffff;
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  list-style-type: none;
}

.prog-assistant-container h3 {
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
  color: #007acc;
}

.prog-assistant-container h4 {
  font-size: 14px;
  font-weight: bold;
  margin-top: 8px;
  color: #555;
}

.prog-assistant-container li {
  padding-left: 15px;
  list-style-type: disc;
}


.prog-assistant-container ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}


.prog-assistant-container li:nth-child(odd) {
  background: #eef2f6;
}

.prog-assistant-container .error-message {
  color: #d9534f;
  font-weight: bold;
}

.prog-assistant-container .info-message {
  color: #5bc0de;
  font-weight: bold;
}

.prog-assistant-container .success-message {
  color: #5cb85c;
  font-weight: bold;
}

/* Responsive Design */
@media (max-width: 768px) {
  .prog-assistant-container {
    max-width: 100%;
  }
}

</style>
