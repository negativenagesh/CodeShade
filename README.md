# CodeShade

[![GitHub stars](https://img.shields.io/github/stars/negativenagesh/CodeShade.svg?style=social)](https://github.com/negativenagesh/CodeShade/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/negativenagesh/CodeShade.svg?style=social)](https://github.com/negativenagesh/CodeShade/network/members)
[![GitHub issues](https://img.shields.io/github/issues/negativenagesh/CodeShade.svg)](https://github.com/negativenagesh/CodeShade/issues)

CodeShade is a fully transparent, frameless desktop gaming application built specifically for **vibecoding**.

<p align="left">
  <img src="assets/CodeShade.gif" alt="CodeShade Demo" width="800" />
</p>

When using agentic coding platforms like Cursor, ClaudeCode, Antigravity, or GitHub Copilot in VSCode, you often have to sit and wait while the AI generates entire files, plans architectures, or runs tests. CodeShade solves that boredom.

It launches a transparent desktop overlay right over your IDE. You can play high-tension, Stake-inspired games (like **Mines**) directly over your codebase. Because the background is completely translucent, you can casually watch your AI agent's cursor move and code as you play so you instantly know when it is done!

## Setup & Installation

We use Docker for the backend game-state server and `uv` to securely execute the frontend desktop application.

### 1. Clone the Repository

First, clone the project to your local machine:

```bash
git clone https://github.com/negativenagesh/CodeShade.git
cd CodeShade
```

### 2. Install Requirements

Ensure you have [uv](https://github.com/astral-sh/uv) installed on your machine to manage dependencies and build the app:

- Install `uv` via: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 3. Build the macOS App

We provide a convenient bash script to install PyInstaller and bundle the application (including the FastAPI server and all frontend assets) into a `.app` file:

```bash
chmod +x build_mac.sh
./build_mac.sh
```

### 4. Launch CodeShade

Once the build is complete, your standalone app will be located in the `dist/` folder.
You can open it directly from the terminal or double-click it in Finder:

```bash
open dist/CodeShade.app
```

_(The transparent client will successfully launch, start the backend automatically, and snap over your active windows)_

> **Running from source**: If you prefer to run CodeShade without building the bundle, simply execute `uv run main.py`.

## Support and Follow

If you enjoy CodeShade and find it useful for your vibecoding setup, please consider supporting the project:

- **Star the repository**: Click the Star button at the top right of this page to show your support!
- **Fork the project**: Click Fork to create your own copy and start contributing or modifying games.
