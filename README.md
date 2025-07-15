# 📡 OSC WebSocket Bridge + p5.js Visualiser

![Raspberry pi pico and cap sensor](/pico_osc_cap.jpeg)              
Physical setup of the pi pico and adafruit cap sensor

This project receives OSC messages (e.g. from a Raspberry Pi Pico) and broadcasts them to connected browsers via WebSockets. The browser uses p5.js to display or respond to incoming OSC data in real time.

---

## 🎯 Project Purpose

The primary goal of this project is to enable **wireless capacitive sensing** — allowing you to embed touch or proximity sensors into physical objects and **transmit the data wirelessly** to a browser-based p5.js visualisation.

This makes it ideal for **interactive installations**, **experimental interfaces**, or **physical computing projects**.

While originally designed for capacitive touch sensing, this framework is **easily adaptable** to other data sources and environments, including:
- Pressure sensors
- Motion detectors
- Sound or light sensors
- Custom sensor setups using OSC

---

## 🧰 Features

- Receives OSC messages via UDP (e.g. from sensors or microcontrollers)
- Broadcasts OSC data to all connected clients using WebSocket
- p5.js frontend for live display or interaction
- Easily accessible on your local network (great for classrooms or workshops)

---

## 🛠️ Requirements

- Node.js (v16+ recommended)
- Devices (e.g. computer, microcontroller) all connected to the **same Wi-Fi network**
- An OSC sender (e.g. a Raspberry Pi Pico sending to port `5000`)

---

## 📁 Folder Structure

```
osc-webapp/
├── wsApp.js              # Node.js server
└── public/
    ├── index.html        # p5.js visualiser
    └── sketch.js         # WebSocket client and p5.js code
```

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/osc-webapp.git
cd osc-webapp
```

### 2. Install dependencies

```bash
npm install express ws node-osc
```

### 3. Run the server

```bash
node wsApp.js
```

You’ll see something like:

```
✅ Server running at: http://192.168.8.170:3000
📡 Listening for OSC on port 5000
```

> **Note:** The IP address shown is your machine’s local IP — use it to connect from other devices on the same network.

---

## 🌐 Access the p5.js App

From **any device on the same Wi-Fi network**, open a browser and visit:

```
http://<your-computer-ip>:3000
```

Example:

```
http://192.168.8.170:3000
```

---

## 📤 Sending OSC

Send OSC messages (e.g. from a Pico, TouchDesigner, Max/MSP, etc.) to:

```
UDP Host: <your-computer-ip>
UDP Port: 5000
```

Example OSC message:

```
Address: /touch
Args: [ 4 ]
```

---

## 🔧 Troubleshooting

- ❌ **WebSocket connection fails?**
  - Make sure the browser is loading over `http://`, not `file://` or `https://`.
  - Check that you're using the correct IP (not `localhost` on a phone).

- ❌ **No OSC data received?**
  - Verify that your sending device is connected to the same network.
  - Double-check that it's sending to the right IP and port (`5000`).

---

## 💡 Customisation

You can modify the `public/sketch.js` file to:
- Animate shapes
- Plot OSC data over time
- Trigger visuals or sounds based on messages

---

## 📄 License

MIT License – use freely and modify as needed.

