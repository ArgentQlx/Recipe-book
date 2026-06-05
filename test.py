import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class DragDropWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Drag & Drop")
        self.setGeometry(100, 100, 300, 200)

        # Компоновка
        layout = QVBoxLayout()
        self.label = QLabel("Перетащите текст сюда", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed black; padding: 20px;")
        
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 1. Включаем приём данных
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # 2. Проверяем, есть ли текст для приёма
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 3. Получаем и обрабатываем данные
        text = event.mimeData().text()
        self.label.setText(text)
        print(f"Принято: {text}")
        event.acceptProposedAction()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragDropWindow()
    window.show()
    sys.exit(app.exec())
