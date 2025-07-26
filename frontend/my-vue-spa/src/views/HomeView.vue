<!-- home.vue -->
<template>
  <div>
    <Navbar />
    <a href="#" class="styled-link">
      Applications Open now for January 2025 Batch | Applications Close: January 02, 2025
      <button class="button">Apply Now</button>
    </a>
    <div class="share-section">
      <span>Share this page with your friends and family on</span>
    </div>
    <div class="share-section">
      <a href="#"><img src="@/Images/fb.png" alt="Facebook" /></a>
      <a href="#"><img src="@/Images/t.png" alt="Twitter" /></a>
      <a href="#"><img src="@/Images/li.png" alt="LinkedIn" /></a>
      <a href="#"><img src="@/Images/tg.png" alt="Telegram" /></a>
      <a href="#"><img src="@/Images/wa.png" alt="WhatsApp" /></a>
      <a href="#"><img src="@/Images/ig.png" alt="Instagram" /></a>
    </div>
    <div class="container">
      <div class="video-section">
        <iframe width="350" height="197" src="https://www.youtube.com/embed/lEMtlAqlJww"></iframe>
      </div>
      <div class="text-section">
        <h1>
          IIT Madras, India's top technical institute, welcomes you to the
          <span class="text-yellow">world's first 4-year Bachelor of Science (BS) Degree in Data Science and Applications</span>
        </h1>
        <p>MFor the first time, you can work towards an undergraduate degree / diploma from an IIT regardless of your age, location, or academic backgrounds.
          More than 36000 students currently studying with us in the program.</p>
      </div>
    </div>
    <div class="slideshow-container">
      <img src="@/Images/display1.png" alt="Image 1" class="active" />
      <img src="@/Images/display2.png" alt="Image 2" />
      <img src="@/Images/display3.png" alt="Image 3" />
      <img src="@/Images/display4.png" alt="Image 4" />
      <img src="@/Images/display5.png" alt="Image 5" />
    </div>
    <!-- Popup container -->
    <div class="popup" v-if="showPopup">
      <button class="close-btn" @click="togglePopup">&times;</button>
      <img src="@/Images/robot.png" alt="AI Assistant">
      <h3>Welcome!</h3>
      <p>Hi there! I’m StudyBuddy! Your AI assistant. I am here to guide you.</p>
      <!-- Modal Body -->
        <div class="chat-container">
          <div class="chat-box" v-for="(message, index) in chatMessages" :key="index">
            <!-- CHANGED: For bot messages, use v-html with markdown parsing -->
            <div v-if="!message.user" v-html="parseMarkdown(message.text)" class="bot-message"></div>
            <div v-else class="user-message">{{ message.text }}</div>
          </div>
        <!-- Chat Input -->
        <div class="chat-modal-input">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="Type your message..."
          />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
    <!-- Chatbot Toggle Button -->
    <img
      src="@/Images/nav-assist.png"
      alt="AI Assistant"
      width="100vh"
      @click="togglePopup"
      class="study-buddy-img"
    />
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import Navbar from "./Navbar.vue";

export default {
  components: {
    Navbar,
  },
  // mounted() {
  //   // Automatically show popup after 1 second
  //   setTimeout(() => {
  //     this.showPopup = true;
  //   }, 1000);
  // },
  data() {
    return {
      showPopup: false,
      userInput: "",
      chatMessages: [{ text: "Hello! How can I assist you today?", user: false }],
    };
  },
  methods: {
    togglePopup() {
      this.showPopup = !this.showPopup;
    },
    
    sendMessage() {
      if (this.userInput.trim() === "") return;
      // Push user message
      this.chatMessages.push({ text: this.userInput, user: true });
      this.getBotResponse(this.userInput);
      this.userInput = "";
    },
    getBotResponse(input) {
      axios
        .post("http://127.0.0.1:5000/api/ask", { question: input })
        .then((response) => {
          // CHANGED: Reduced delay to 1s for a faster feel
          setTimeout(() => {
            if (response.data && response.data.answer) {
              this.chatMessages.push({ text: response.data.answer, user: false });
            } else {
              this.chatMessages.push({ text: "Sorry, no answer received.", user: false });
            }
          }, 1000);
        })
        .catch((error) => {
          console.error("Error getting response: ", error);
          setTimeout(() => {
            this.chatMessages.push({
              text: "Error: Could not connect to the chatbot.",
              user: false,
            });
          }, 1000);
        });
    },
    // ADDED: Parse markdown into HTML
    parseMarkdown(text) {
      return marked.parse(text);
    },
  },
};
</script>

<style scoped>
/* Chatbot Modal Popup */
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70vw;               /* Increased width */
  max-width: 1200px;          /* Max width for larger screens */
  height: 80vh;               /* Increased height */
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

/* Close Button */
.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: transparent;
  border: none;
  font-size: 28px;
  color: #555;
  cursor: pointer;
}

.close-btn:hover {
  color: #000;
}

/* Chat Container */
.chat-container {
  flex: 1;
  max-height: calc(80vh - 150px); /* Adjust height based on modal size */
  overflow-y: auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: inset 0 0 10px #ddd;
}

/* Individual Message Box */
.chat-box {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

/* User Messages */
.user-message {
  background-color: #d1e7dd;
  color: #155724;
  padding: 10px 15px;
  border-radius: 10px;
  align-self: flex-end;
  text-align: right;
  max-width: 70%;
  word-wrap: break-word;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Bot Messages */
.bot-message {
  background-color: #f1f1f1;
  color: #333;
  padding: 10px 15px;
  border-radius: 10px;
  align-self: flex-start;
  text-align: left;
  max-width: 70%;
  word-wrap: break-word;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Chat Input Section */
.chat-modal-input {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #fff;
  border-top: 1px solid #ddd;
}

/* Input Field */
.chat-modal-input input {
  flex: 1;
  padding: 12px 15px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s;
}

.chat-modal-input input:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.3);
}

/* Send Button */
.chat-modal-input button {
  padding: 12px 25px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.chat-modal-input button:hover {
  background-color: #0056b3;
}

/* Chatbot Toggle Button */
.study-buddy-img {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 80px;
  height: 80px;
  cursor: pointer;
  transition: transform 0.3s;
}

.study-buddy-img:hover {
  transform: scale(1.1);
}

/* Scrollbar Styling */
.chat-container::-webkit-scrollbar {
  width: 10px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #999;
}

/* Responsive Styling */
@media (max-width: 768px) {
  .popup {
    width: 90vw;
    height: 90vh;
  }

  .user-message, .bot-message {
    max-width: 90%;
  }

  .chat-modal-input input {
    font-size: 14px;
    padding: 10px;
  }

  .chat-modal-input button {
    padding: 10px 20px;
    font-size: 14px;
  }
}

</style>