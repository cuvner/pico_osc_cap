let wsStatus = "Connecting...";
let latestOSC = "";

function setup() {
  createCanvas(400, 200);
  textSize(18);
  connectWebSocket();
}

function draw() {
  background(255);
  fill(0);
  text("WebSocket: " + wsStatus, 10, 30);
  text("Latest OSC: " + latestOSC, 10, 70);
}

function connectWebSocket() {
  const wsURL = "ws://192.168.8.170:3000"; // ✅ Hardcoded working IP

  let socket;

  try {
    socket = new WebSocket(wsURL);
  } catch (e) {
    console.error("WebSocket failed to connect:", e.message);
    wsStatus = "Invalid WebSocket URL";
    return;
  }

  socket.onopen = function (event) {
    console.log("✅ WebSocket connected:", event);
    wsStatus = "Connected";
  };

  socket.onmessage = function (event) {
    try {
      let msg = JSON.parse(event.data);
      console.log("OSC →", msg);
      handleOscData(msg);
    } catch (e) {
      console.error("❌ Failed to parse OSC message:", e);
    }
  };

  socket.onerror = function (error) {
    console.log("❌ WebSocket error:", error);
    wsStatus = "Error";
  };

  socket.onclose = function (event) {
    if (event.wasClean) {
      wsStatus = "Closed";
    } else {
      wsStatus = "Disconnected";
    }
  };
}

function handleOscData(msg) {
  if (Array.isArray(msg)) {
    latestOSC = msg[0] + ": " + msg.slice(1).join(", ");
  } else {
    latestOSC = "Invalid OSC format";
  }
}
