import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

class TransparentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(300, 300)
        self.label = QLabel("Drag me!", self)
        self.label.move(100, 100)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentApp()
    window.show()
    sys.exit(app.exec())
