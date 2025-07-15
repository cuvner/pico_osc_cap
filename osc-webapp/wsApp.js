const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const osc = require('node-osc');
const os = require('os');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const PORT = 3000;
const oscPort = 5000;

app.use(express.static('public')); // Serve frontend from 'public' folder

// OSC server
const oscServer = new osc.Server(oscPort, '0.0.0.0');
oscServer.on("message", function (msg, rinfo) {
  console.log("Received OSC message:", msg);
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(msg));
    }
  });
});

// Get local IP
function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const iface of Object.values(interfaces)) {
    for (const alias of iface) {
      if (alias.family === 'IPv4' && !alias.internal) {
        return alias.address;
      }
    }
  }
  return '0.0.0.0';
}

const localIP = getLocalIP();
server.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running at: http://${localIP}:${PORT}`);
  console.log(`📡 Listening for OSC on port ${oscPort}`);
});
