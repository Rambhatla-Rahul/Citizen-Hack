import React from 'react';
import { BsChatSquareTextFill } from "react-icons/bs";

// Define the API URL
const apiUrl = 'http://localhost:8000/'; // Match this with your Flask backend's API URL

const ChatbotComponent = () => {
  // Function to open the chatbot in a new tab
  const openChatbot = () => {
    // Open the chatbot interface from the backend URL
    window.open(apiUrl, '_blank');
  };

  return (
    <div 
      className='w-[100px] h-[100px] flex items-center justify-center mr-14 mb-10 rounded-full' 
      id="chat-icon-container"
      onClick={openChatbot}
    >
      {/* Button to trigger opening the chatbot */}
      <button 
        className='text-4xl' 
         // Call the function to open the chatbot
      >
        <BsChatSquareTextFill />
      </button>
    </div>
  );
}

export default ChatbotComponent;
