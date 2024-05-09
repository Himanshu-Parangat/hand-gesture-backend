# Hand Detection Backend

This project is a flexible backend that provides hand detection capabilities
to web applications via WebSockets. It allows developers to easily integrate
hand detection functionality into their applications without the need to 
implement complex computer vision algorithms themselves.

## Features

- Real-time hand detection using computer vision media
- WebSocket-based communication for efficient and low-latency data transfer
- Flexible and easy integration with web applications
- Cross-platform compatibility (works on various operating systems and devices)


## Features

- Real-time hand detection using OpenCV computer vision and MediaPipe
- WebSocket-based communication for efficient and low-latency data transfer
- FastAPI/ Swagger for the backend API 
- Flexible and easy integration with web applications
- Cross-platform compatibility (works on various operating systems and devices)
- High-performance multi-threaded architecture


## project structure
```bash
.
├── LICENSE.md
├── README.md
├── requirements.txt
├── src
│   ├── camera_handlers.py
│   ├── config
│   │   ├── default_config.json
│   │   └── user_config.json
│   ├── config_handlers.py
│   ├── drawing_handlers.py
│   ├── endpoint_handlers.py
│   ├── handtracker_handlers.py
│   ├── main.py
│   ├── model_handlers.py
│   ├── state_handlers.py
│   └── websockets_handlers.py
└── test

4 directories, 14 files
```


## Getting Started

1. Clone the repository:

```bash
https://github.com/Himanshu-Parangat/hand-gesture-backend && cd hand-gesture-backend
```

2. Install dependencies:

```bash
pip Install -r ./requirements.txt 
```

3. run main file:

```bash
python3 main.py
```
