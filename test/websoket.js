window.addEventListener('DOMContentLoaded', function() {
  const socket = new WebSocket("ws://localhost:8001");
  const messagesContainer = document.getElementById("messages");
  let messageCounter = 1;

  socket.onopen = function() {
    console.log("WebSocket connection opened");
    printMessage("WebSocket connection opened");
  };

  socket.onmessage = function(event) {
    printMessage(`${messageCounter}. ${event.data}`);
    messageCounter++;
  };

  socket.onclose = function(event) {
    console.log("WebSocket connection closed with code:", event.code);
    printMessage(`WebSocket connection closed with code: ${event.code}`);
  };

  socket.onerror = function(error) {
    console.error("WebSocket error:", error);
    printMessage(`WebSocket error: ${error}`);
  };

  function printMessage(message) {
    const messageElement = document.createElement("p");
    messageElement.textContent = message;
    messagesContainer.appendChild(messageElement);
  }
});
