import os
import requests
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QLabel, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

def play_sound(name):
    base_dir = os.path.join(os.getcwd(), "backend", "games", "mines", "sounds")
    try:
        if name == "Glass":
            subprocess.Popen(["afplay", os.path.join(base_dir, "diamond_trimmed.wav")])
        elif name == "Basso":
            subprocess.Popen(["afplay", os.path.join(base_dir, "bomb_trimmed.wav")])
        elif name == "Tink":
            subprocess.Popen(["afplay", "/System/Library/Sounds/Tink.aiff"])
        elif name == "Hero":
            subprocess.Popen(["afplay", "/System/Library/Sounds/Hero.aiff"])
    except:
        pass

def get_tile_style(state="hidden"):
    # Heavily increased size for better visibility
    base_dim = 80 
    
    if state == "hidden":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 200);
            border-radius: 8px;
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        QPushButton:hover {{
            background-color: rgba(40, 54, 68, 200);
        }}
        """
    elif state == "gem":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 200);
            border-radius: 8px;
            color: #00E701;
            font-size: 32px;
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        """
    elif state == "dimmed_gem":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 80);
            border-radius: 8px;
            color: rgba(0, 231, 1, 80);
            font-size: 32px;
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        """
    elif state == "bomb":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 200);
            border-radius: 8px;
            color: #FF2B2B;
            font-size: 32px;
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        """
    elif state == "bomb_hit":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 200);
            border-radius: 8px;
            color: #FF2B2B;
            font-size: 55px; /* Making exact selected bomb stand out! */
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        """
    elif state == "dimmed_bomb":
        return f"""
        QPushButton {{
            background-color: rgba(30, 40, 50, 80); /* Shaded out background */
            border-radius: 8px;
            color: rgba(255, 43, 43, 80); /* Shaded out emoji */
            font-size: 32px;
            min-width: {base_dim}px;
            min-height: {base_dim}px;
        }}
        """

class MinesGame(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.game_id = None
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # LEFT PANEL
        left_panel = QVBoxLayout()
        
        self.mult_lbl = QLabel("1.00x")
        self.mult_lbl.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        left_panel.addWidget(self.mult_lbl)

        # Bet input
        lbl_bet = QLabel("Bet Amount")
        lbl_bet.setStyleSheet("color: #a0a0a0;")
        left_panel.addWidget(lbl_bet)
        self.inp_bet = QLineEdit("10.00")
        self.inp_bet.setStyleSheet("background: rgba(0,0,0,100); color: white; padding: 5px; border-radius: 4px;")
        left_panel.addWidget(self.inp_bet)

        # Mines dropdown
        lbl_mines = QLabel("Mines")
        lbl_mines.setStyleSheet("color: #a0a0a0;")
        left_panel.addWidget(lbl_mines)
        self.combo_mines = QComboBox()
        self.combo_mines.addItems([str(i) for i in range(1, 25)])
        self.combo_mines.setCurrentText("3")
        self.combo_mines.setStyleSheet("background: rgba(0,0,0,100); color: white; padding: 5px; border-radius: 4px;")
        left_panel.addWidget(self.combo_mines)
        
        # Start game / Cashout
        self.btn_action = QPushButton("Start Game")
        self.btn_action.setStyleSheet("background: #00E701; color: black; font-weight: bold; border-radius: 5px; padding: 10px;")
        self.btn_action.clicked.connect(self.handle_action)
        left_panel.addWidget(self.btn_action)

        left_panel.addStretch()
        
        btn_back = QPushButton("Back")
        btn_back.setStyleSheet("background: rgba(255,255,255,10); color: white; padding: 5px; border-radius: 4px;")
        btn_back.clicked.connect(lambda: self.main_window.switch_game(0))
        left_panel.addWidget(btn_back)

        main_layout.addLayout(left_panel)

        # RIGHT PANEL - 5x5 GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.tiles = []
        for i in range(25):
            btn = QPushButton("")
            btn.setStyleSheet(get_tile_style("hidden"))
            btn.clicked.connect(lambda checked, idx=i: self.pick_tile(idx))
            btn.setEnabled(False)
            self.grid.addWidget(btn, i // 5, i % 5)
            self.tiles.append(btn)
            
        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)

    def handle_action(self):
        if self.game_id is None:
            self.start_game()
        else:
            self.cashout()

    def start_game(self):
        play_sound("Tink")
        try:
            bet = float(self.inp_bet.text())
            bombs = int(self.combo_mines.currentText())
            r = requests.post(f"{BACKEND_URL}/mines/start", json={"bet": bet, "bombs": bombs})
            if r.status_code == 200:
                data = r.json()
                self.game_id = data["game_id"]
                self.mult_lbl.setText("1.00x")
                self.btn_action.setText(f"Cashout (1.00x)")
                self.combo_mines.setEnabled(False)
                self.inp_bet.setEnabled(False)
                
                # Reset tiles
                for btn in self.tiles:
                    btn.setText("")
                    btn.setIcon(QIcon())
                    btn.setStyleSheet(get_tile_style("hidden"))
                    btn.setEnabled(True)
        except Exception as e:
            pass

    def pick_tile(self, idx):
        if self.game_id is None: return
        
        try:
            r = requests.post(f"{BACKEND_URL}/mines/pick", json={"game_id": self.game_id, "index": idx})
            if r.status_code == 200:
                data = r.json()
                self.tiles[idx].setEnabled(False)
                picked = data["picked"]
                
                if data["status"] == "boom":
                    play_sound("Basso")
                    self.reveal_board(data["board"], picked, hit_idx=idx)
                    self.end_game_ui()
                else:
                    play_sound("Glass")
                    self.tiles[idx].setText("")
                    icon_path = os.path.join(os.getcwd(), "backend", "games", "mines", "diamond.svg")
                    self.tiles[idx].setIcon(QIcon(icon_path))
                    self.tiles[idx].setIconSize(QSize(60, 60))
                    self.tiles[idx].setStyleSheet(get_tile_style("gem"))
                    
                    if data["status"] == "cashout":
                        play_sound("Hero")
                        self.reveal_board(data["board"], picked)
                        self.end_game_ui()
                    else:
                        m = data["multiplier"]
                        self.mult_lbl.setText(f"{m}x")
                        self.btn_action.setText(f"Cashout ({m}x)")
        except Exception as e:
            pass

    def cashout(self):
        if self.game_id is None: return
        try:
            r = requests.post(f"{BACKEND_URL}/mines/cashout", json={"game_id": self.game_id})
            if r.status_code == 200:
                play_sound("Hero")
                data = r.json()
                self.reveal_board(data["board"], data["picked"])
                self.end_game_ui()
        except Exception as e:
            pass
            
    def end_game_ui(self):
        self.game_id = None
        self.combo_mines.setEnabled(True)
        self.inp_bet.setEnabled(True)
        self.btn_action.setText("Start Game")
        for btn in self.tiles:
            btn.setEnabled(False)

    def reveal_board(self, board, picked_indices, hit_idx=None):
        for i, val in enumerate(board):
            if val == "bomb":
                self.tiles[i].setText("")
                bomb_path = os.path.join(os.getcwd(), "backend", "games", "mines", "bomb.svg")
                self.tiles[i].setIcon(QIcon(bomb_path))
                self.tiles[i].setIconSize(QSize(60, 60))
                if i == hit_idx:
                    self.tiles[i].setStyleSheet(get_tile_style("bomb_hit"))
                else:
                    self.tiles[i].setStyleSheet(get_tile_style("dimmed_bomb"))
            elif val == "safe":
                self.tiles[i].setText("")
                icon_path = os.path.join(os.getcwd(), "backend", "games", "mines", "diamond.svg")
                self.tiles[i].setIcon(QIcon(icon_path))
                self.tiles[i].setIconSize(QSize(60, 60))
                if i in picked_indices:
                    self.tiles[i].setStyleSheet(get_tile_style("gem"))
                else:
                    self.tiles[i].setStyleSheet(get_tile_style("dimmed_gem"))
