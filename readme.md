# PicoShooter

An online **move-and-shoot** game server written in C, designed to work with clients based on **Raspberry Pi Pico** (analog joystick input + LCD rendering).

## About The Project

The goal is to support a lightweight real-time multiplayer game where:

- the player moves using a joystick,
- the player can shoot,
- the client (Pi Pico + LCD) sends input and receives world state updates,
- the server handles game logic, synchronization, and networking.

## Current Status

The repository currently contains a basic TCP server implementation:

- listens on port `5000`,
- handles multiple clients via threads (`pthread`),
- uses a test **echo** communication model (server sends back received data).

This is a solid starting point for implementing the actual game protocol.

## Project Structure

```text
PicoShooter/
├── readme.md
└── server/
		└── server.c
```

## Quick Start (Linux / WSL)

### 1. Build The Server

```bash
cd server
gcc -O2 -Wall -Wextra -pthread server.c -o picoshooter_server
```

### 2. Run

```bash
./picoshooter_server
```

The server listens on `0.0.0.0:5000`.

### 3. Quick Client Test

In a second terminal:

```bash
nc 127.0.0.1 5000
```

The data you type should be echoed back by the server.

## Target Game Architecture

Planned responsibility split:

- **Client (Pi Pico)**:
	- reads analog joystick axes,
	- maps input to commands (`MOVE_X`, `MOVE_Y`, `SHOOT`),
	- renders game state on LCD,
	- communicates with the server.
- **Server (C)**:
	- authoritative world logic (player positions, bullets, collisions),
	- tick rate and state updates,
	- multi-connection handling,
	- state broadcast to clients.

## Simple Protocol Proposal (MVP)

Example text messages (easy to debug):

- client -> server:
	- `HELLO <nick>`
	- `INPUT <dx> <dy> <shoot>`
- server -> client:
	- `WELCOME <id>`
	- `STATE <tick> <players...> <bullets...>`
	- `HIT <attacker_id> <victim_id>`

At a later stage, it is worth moving to a compact binary format for lower latency.

## Roadmap

- [ ] Add player and bullet data structures.
- [ ] Implement the main game loop (tick).
- [ ] Replace echo behavior with real command handling.
- [ ] Add validation for client input data.
- [ ] Add timeout-based disconnect for inactive clients.
- [ ] Build the Pico client (joystick + LCD + networking).
- [ ] Add logging and basic integration tests.

## Requirements

- C compiler (e.g., GCC)
- POSIX Threads library (`pthread`)
- Linux / Unix system or a compatible environment (e.g., WSL)

## Security And Stability Note

The current server version is a development build and still needs production-level improvements:

- safer buffer management,
- better error handling (`socket`, `bind`, `accept`, `recv`),
- proper synchronization of shared game state,
- protection against malformed client packets.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
