import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from ui.components import MainMenu, GamesList
from ui.games.mines_view import MinesGame

class TransparentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties for transparency
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.resize(600, 600)
        
        # Central widget with stacked layout to swap games
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.central_layout.addWidget(self.stack)
        
        # Initialize views
        self.menu_view = MainMenu(self)
        self.games_view = GamesList(self)
        self.mines_view = MinesGame(self)
        
        self.stack.addWidget(self.menu_view)     # Index 0
        self.stack.addWidget(self.games_view)    # Index 1
        self.stack.addWidget(self.mines_view)    # Index 2
        

    def switch_game(self, index: int):
        self.stack.setCurrentIndex(index)
        # Adjust size for mines view
        if index == 2:
            self.resize(850, 750)
        else:
            self.resize(600, 600)

    # Implemented drag logic so window can be moved despite lacking a title bar
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()

import multiprocessing

def start_backend():
    import uvicorn
    from backend.main import app as fastapi_app
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Start the backend server programmatically
    server_process = multiprocessing.Process(target=start_backend, daemon=True)
    server_process.start()

    app = QApplication(sys.argv)
    window = TransparentApp()
    window.show()
    sys.exit(app.exec())
