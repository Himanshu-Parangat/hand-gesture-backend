# Hand Detection Backend

This project is a flexible backend that provides hand detection capabilities
to web applications via WebSockets. It allows developers to easily integrate
hand detection functionality into their applications without the need to 
implement complex computer vision algorithms themselves.


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
├── non_blockig.py
├── README.md
├── requirements.txt
├── run.py
├── src
│   ├── configuration
│   │   ├── config_handlers.py
│   │   ├── __init__.py
│   │   ├── model_handlers.py
│   │   └── schema
│   │       ├── default_config.json
│   │       └── user_config.json
│   ├── endpoint
│   │   ├── endpoint_handlers.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── state
│   │   ├── __init__.py
│   │   ├── state.db
│   │   └── state_store.py
│   ├── state_handlers.py
│   ├── tracking
│   │   ├── camera_handlers.py
│   │   ├── drawing_handlers.py
│   │   ├── handtracker_handlers.py
│   │   └── __init__.py
│   └── ws
│       ├── __init__.py
│       └── websockets_handlers.py
└── test
    ├── hooks.html
    └── websoket.js

13 directories, 43 files (includ hidden)

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
