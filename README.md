# CodeShade

[![GitHub stars](https://img.shields.io/github/stars/negativenagesh/CodeShade.svg?style=social)](https://github.com/negativenagesh/CodeShade/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/negativenagesh/CodeShade.svg?style=social)](https://github.com/negativenagesh/CodeShade/network/members)
[![GitHub issues](https://img.shields.io/github/issues/negativenagesh/CodeShade.svg)](https://github.com/negativenagesh/CodeShade/issues)

CodeShade is a fully transparent, frameless desktop gaming application built specifically for **vibecoding**.

When using agentic coding platforms like Cursor, ClaudeCode, Antigravity, or GitHub Copilot in VSCode, you often have to sit and wait while the AI generates entire files, plans architectures, or runs tests. CodeShade solves that boredom.

It launches a transparent desktop overlay right over your IDE. You can play high-tension, Stake-inspired games (like **Mines**) directly over your codebase. Because the background is completely translucent, you can casually watch your AI agent's cursor move and code as you play so you instantly know when it is done!

## Support and Follow

If you enjoy CodeShade and find it useful for your vibecoding setup, please consider supporting the project:

- **Star the repository**: Click the Star button at the top right of this page to show your support!
- **Fork the project**: Click Fork to create your own copy and start contributing or modifying games.

## Setup & Installation

We use Docker for the backend game-state server and `uv` to securely execute the frontend desktop application.

### 1. Clone the Repository

First, clone the project to your local machine:

```bash
git clone https://github.com/negativenagesh/CodeShade.git
cd CodeShade
```

### 2. Install Requirements

Ensure you have the following installed on your machine:
- [Docker](https://www.docker.com/) (Includes Docker Compose)
- [uv](https://github.com/astral-sh/uv) (Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 3. Start the Backend

Our backend container uses an optimized `debian-slim` base that binds the environment dynamically via `uv`. Boot it up in the background:

```bash
docker compose up -d --build
```
*(This starts the FastAPI game state server on `http://localhost:8000`)*

### 4. Launch CodeShade

Start the transparent frontend app overlay using `uv`:

```bash
uv run main.py
```
*(The transparent client will successfully launch and snap directly over your active IDE)*

## Games and Features

- **Mines (Stake Parity)**: A faithfully recreated 5x5 Mines game including authentic zero-latency macOS hit chimes, exact nCr-based multiplier mathematics, and premium flat-vector graphics.
- **True Transparency**: Frameless PyQt6 overlay that naturally integrates into your workflow. Minimalist UI approach: no borders, heavy shadows, or visual bloat.
- **Blazing Fast Backend**: Containerized FastAPI microservice backend managing game session state and provably fair multi-stage logic.
- **Zero-Friction Environment**: Powered entirely by Astral's `uv`. No venv headaches, no massive standard requirements installs.
