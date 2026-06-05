from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

list_widget = QListWidget()

# Добавляем элементы
item1 = QListWidgetItem("Элемент 1")
item2 = QListWidgetItem("Элемент 2")

# ВКЛЮЧАЕМ ВОЗМОЖНОСТЬ РЕДАКТИРОВАНИЯ
item1.setFlags(item1.flags() | Qt.ItemFlag.ItemIsEditable)
item2.setFlags(item2.flags() | Qt.ItemFlag.ItemIsEditable)

list_widget.addItem(item1)
list_widget.addItem(item2)

layout.addWidget(list_widget)
window.setLayout(layout)
window.show()
app.exec()