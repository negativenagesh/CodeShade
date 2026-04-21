import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QScrollArea
)
from PyQt6.QtCore import Qt
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

def get_box_style():
    # Only transparent boxes, no borders, no colors
    return """
    QWidget {
        background-color: rgba(255, 255, 255, 15);
        border: none;
        border-radius: 8px;
        color: rgba(255, 255, 255, 200);
        padding: 15px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 1px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 30);
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 10);
    }
    """

def get_title_style():
    return """
    QLabel {
        background-color: rgba(255, 255, 255, 10);
        border: none;
        border-radius: 8px;
        color: rgba(255, 255, 255, 230);
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    """

class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title box
        self.title = QLabel("CodeShade")
        self.title.setStyleSheet(get_title_style())
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        # Games button box
        btn_games = QPushButton("Games")
        btn_games.setStyleSheet(get_box_style())
        btn_games.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_games.clicked.connect(lambda: self.main_window.switch_game(1))
        layout.addWidget(btn_games)
        
        # Exit button box
        btn_close = QPushButton("Exit")
        btn_close.setStyleSheet(get_box_style())
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.main_window.close)
        layout.addWidget(btn_close)

        # Help Drag Label (transparent, no box)
        self.help = QLabel("(Drag to move)")
        self.help.setStyleSheet("color: rgba(255,255,255,100); font-size: 11px; background: transparent;")
        self.help.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.help)

        self.setLayout(layout)

class GamesList(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title = QLabel("available games")
        self.title.setStyleSheet(get_title_style())
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.games_area = QLabel("fetching...")
        self.games_area.setStyleSheet(get_box_style())
        self.games_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.games_area)

        # Back button
        btn_back = QPushButton("back")
        btn_back.setStyleSheet(get_box_style())
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.main_window.switch_game(0))
        layout.addWidget(btn_back)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.fetch_games()

    def fetch_games(self):
        try:
            r = requests.get(f"{BACKEND_URL}/games")
            if r.status_code == 200:
                data = r.json()
                games = data.get("games", [])
                
                # Clear placeholder
                self.games_area.setParent(None)
                
                # Add a Mines button if its in the backend list
                if "Mines" in games:
                    btn_mines = QPushButton("play mines")
                    btn_mines.setStyleSheet(get_box_style())
                    btn_mines.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_mines.clicked.connect(lambda: self.main_window.switch_game(2))
                    self.layout().insertWidget(1, btn_mines)
                else:
                    self.title.setText("no games available.")
            else:
                self.title.setText("backend error.")
        except Exception:
            self.title.setText("backend offline.")
