<template>
  <div>
    <!-- Sidebar -->
    <div class="sidebar">
      <a href="/coursespage"><img src="@/Images/Icon-01.svg" alt="Icon 1" /></a>
      <a href="#"><img src="@/Images/Icon-02.svg" alt="Icon 2" /></a>
      <a href="#"><img src="@/Images/Icon-03.svg" alt="Icon 3" /></a>
      <a href="#"><img src="@/Images/Icon-04.svg" alt="Icon 4" /></a>
      <a href="#"><img src="@/Images/Icon-05.svg" alt="Icon 5" /></a>
      <a href="#"><img src="@/Images/Icon-06.svg" alt="Icon 6" /></a>
      <a href="#"><img src="@/Images/Icon-07.svg" alt="Icon 7" /></a>
      <a href="#"><img src="@/Images/Icon-08.svg" alt="Icon 8" /></a>
      <a href="#"><img src="@/Images/Icon-09.svg" alt="Icon 9" /></a>
      <a href="#"><img src="@/Images/Icon-10.svg" alt="Icon 10" /></a>
      <a href="#"><img src="@/Images/Icon-11.svg" alt="Icon 11" /></a>
    </div>

    <!-- Main Content -->
    <div class="main-content_1">
      <!-- Search Bar with AI Assistant -->
      <div class="search-bar">
        <input
          type="text"
          v-model="userInput"
          placeholder="Search courses..."
          @click="showPopup = true"
          @keyup.enter="sendMessage"
        />
      </div>

      <!-- AI Assistant Modal -->
      <div v-if="showPopup" class="modal-overlay">
        <div class="modal-content">
          <button class="close-btn" @click="togglePopup">&times;</button>
          <div class="modal-header">
            <h2>StudyBuddy AI Assistant</h2>
            <p>How can I help you today?</p>
          </div>
          <div class="chat-container">
            <div v-for="(message, index) in chatMessages" :key="index">
              <div v-if="message.user" class="chat-box user-message">
                <span>{{ message.text }}</span>
              </div>
              <div v-else class="chat-box bot-message">
                <span v-html="message.text"></span>
              </div>
            </div>
          </div>
          <div class="chat-input">
            <input
              type="text"
              v-model="userInput"
              placeholder="Type your message..."
              @keyup.enter="sendMessage"
            />
            <button @click="sendMessage">Send</button>
          </div>
        </div>
      </div>

      <!-- Sub Content -->
      <div class="sub-content">
        <div class="latest-updates">
          <h2>Latest Updates</h2>
          <ul>
            <li>Update 1: New course on Data Science available now!</li>
            <li>Update 2: Python course has new assignments.</li>
            <li>Update 3: Join the upcoming webinar on AI.</li>
          </ul>
        </div>

        <div class="content_1">
          <h1>My current courses</h1>
          <div class="course-card_1">
            <h2>Programming in Python</h2>
            <p>Course Description</p>
            <router-link to="/python" class="button">Go to Course</router-link>
          </div>
          <div class="course-card_1">
            <h2>English for DS</h2>
            <p>Course Description</p>
            <router-link to="/english" class="button">Go to Course</router-link>
          </div>
          <router-link to="/coursespage">VIEW ALL COURSES</router-link>
        </div>

        <!-- Peer Study Group Recommendation -->
        <div>
          <img
            src="@/Images/peer-group.png"
            alt="AI Assistant"
            width="150px"
            @click="togglePeerRecommendations"
            class="peer-group-img"
          />
          <div class="peer-study-group" v-if="showPeerRecommendations">
            <h2>Peer Study Group Recommendations</h2>
            <ul>
              <li v-if="peerList.length === 0">No recommendations available</li>
              <li v-for="(peer, index) in peerList" :key="index">
                <strong>Peer {{ index + 1 }}</strong><br />
                Name: {{ peer.name }}<br />
                Email: {{ peer.email }}
              </li>
            </ul>
          </div>
        </div>
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
      showPopup: false,
      userInput: '',
      chatMessages: [],
      showPeerRecommendations: false,
      peerList: []
    };
  },
  mounted() {
    const email = localStorage.getItem('userEmail');
    if (email) {
      const rollNo = localStorage.getItem('rollNo');
      this.fetchPeerGroup(rollNo);
    }
  },
  methods: {
    togglePopup() {
      this.showPopup = !this.showPopup;
    },
    formatBotResponse(response) {
    let paragraphs = response.split(/\n\s*\n/);
    paragraphs = paragraphs.map(paragraph => {
      let formattedParagraph = paragraph;
      formattedParagraph = formattedParagraph.replace(/\*+\s*/g, ''); 
      formattedParagraph = formattedParagraph.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); 
      formattedParagraph = formattedParagraph.replace(/_(.*?)_/g, '<em>$1</em>'); 

      return `<p>${formattedParagraph}</p>`;
    });

    return paragraphs.join('\n');
  },
    
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      this.chatMessages.push({ text: this.userInput, user: true });

      try {
        const response = await fetch("http://127.0.0.1:5000/api/prompt_search", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: this.userInput })
        });

        const data = await response.json();

        if (data.error) {
          this.chatMessages.push({ text: data.error, user: false });
        } else {
          const formattedResponse = this.formatBotResponse(data.ai_response);
          this.chatMessages.push({ text: formattedResponse, user: false });
        }
      } catch (err) {
        console.error("Error:", err);
        this.chatMessages.push({
          text: "Sorry, I couldn't process your request. Please try again.",
          user: false
        });
      }

      this.userInput = "";
    },
    togglePeerRecommendations() {
      this.showPeerRecommendations = !this.showPeerRecommendations;
    },
    async fetchPeerGroup(rollNo) {
      try {
        const response = await fetch('http://localhost:5000/api/study-group-recommendation', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ roll_no: rollNo })
        });

        const data = await response.json();
        this.peerList = data.response;
      } catch (err) {
        console.error('Error fetching peer group:', err);
      }
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 30px;
  width: 1000px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  position: relative;
  max-height: 100vh;
  overflow-y: auto;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #000;
}

.chat-container {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.chat-box {
  padding: 10px;
  border-radius: 8px;
  margin: 10px 0;
}

.user-message {
  background: #d1e7dd;
  align-self: flex-end;
}

.bot-message {
  background: #f8d7da;
  align-self: flex-start;
  text-align: left;
}

.chat-input {
  display: flex;
  justify-content: space-between;
}
</style>