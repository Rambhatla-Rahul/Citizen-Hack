const generateButton = document.getElementById('generate-button');

generateButton.addEventListener('click', () => {
  // Run the JavaScript code here
  const WebSocket = require('ws');
  const ws = new WebSocket('ws://localhost:8080');

  let text = '';

  ws.on('message', (message) => {
    text = message;
  });

  ws.on('open', () => {
    console.log('Connected to WebSocket server');
  });

  ws.on('error', (error) => {
    console.error('Error occurred:', error);
  });

  // Use the received text here
  console.log(text);
});