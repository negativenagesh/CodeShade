#!/bin/bash
set -e

echo "Ensuring pyinstaller is installed..."
uv pip install pyinstaller

echo "Building macOS .app bundle..."
uv run python -m PyInstaller --noconfirm --windowed \
  --name "CodeShade" \
  --add-data "assets:assets" \
  --hidden-import="uvicorn.logging" \
  --hidden-import="uvicorn.loops" \
  --hidden-import="uvicorn.loops.auto" \
  --hidden-import="uvicorn.protocols" \
  --hidden-import="uvicorn.protocols.http" \
  --hidden-import="uvicorn.protocols.http.auto" \
  --hidden-import="uvicorn.protocols.websockets" \
  --hidden-import="uvicorn.protocols.websockets.auto" \
  --hidden-import="uvicorn.lifespan" \
  --hidden-import="uvicorn.lifespan.on" \
  main.py

echo "Build complete! Your app is located at: dist/CodeShade.app"
echo "To distribute via Homebrew, zip this file and update your Cask formula."
