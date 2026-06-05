from PyQt6.QtWidgets import QWidget, QGridLayout, QTextBrowser, QPushButton
from PyQt6.QtCore import Qt

class ModalWindow(QWidget):
    def __init__(self, label_text: str, signal):
        super().__init__()

        self.setWindowTitle('Подтвердите')

        label = QTextBrowser()
        label.setText(label_text)
        self.yes_btn = QPushButton('Да')
        self.no_btn = QPushButton('Нет')

        self.signal = signal

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 4)
        layout.addWidget(self.yes_btn, 1, 0, 1, 2)
        layout.addWidget(self.no_btn, 1, 2, 1, 2)

        self.setLayout(layout)

        self.no_btn.clicked.connect(self.close)
        self.yes_btn.clicked.connect(self.yes_confirm)
        self.no_btn.setProperty('class', 'cancel_btn')
        label.setProperty('class', 'modal_label')

        self.show()

    def yes_confirm(self):
        self.signal.emit()
        self.close()