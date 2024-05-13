from src import main
import asyncio

'''
.
├── LICENSE.md
├── README.md
├── requirements.txt
├── run.py
├── src
│   ├── config
│   │   ├── config_handlers.py
│   │   ├── model_handlers.py
│   │   └── schema
│   │       ├── default_config.json
│   │       └── user_config.json
│   ├── detection
│   │   ├── camera_handlers.py
│   │   ├── drawing_handlers.py
│   │   └── handtracker_handlers.py
│   ├── endpoint
│   │   └── endpoint_handlers.py
│   ├── state_handlers.py
│   └── ws
│       └── websockets_handlers.py
└── test
    ├── hooks.html
    └── websoket.js

8 directories, 16 files
'''


if __name__ == "__main__":
    asyncio.run(main())

