# Python Chatroom Application

A simple multithreaded chatroom built using Python's `socket`, `threading`, and `tkinter` libraries. This app allows multiple clients to connect to a central server and exchange messages in real time.

---

## Features

- Command-line chat support
- Graphical User Interface (GUI) for clients using `tkinter`
- Multi-client broadcasting using threads
- Graceful client exit with `QUIT` command
- Basic chat logging in the terminal

---

## Files

- `server.py`: Launches the chatroom server.
- `client.py`: Connects to the server and enables chat via CLI and GUI.

---

## How to Run

1. Start the Server

```bash
python server.py 127.0.0.1 -p 1060
```

- `127.0.0.1` is the host (localhost by default).
- `1060` is the port number (can be changed).

---

2. Start a Client

```bash
python client.py 127.0.0.1 -p 1060
```

- On running, the client will ask for your name.
- Type messages in the GUI or terminal.
- Type `QUIT` to leave the chatroom.

---
Notes:
- Ensure server is started **before** any clients connect.
- Multiple clients can connect and chat simultaneously.
- Server prints all incoming/outgoing messages and logs connection status.
