from PyQt6.QtWidgets import QListWidget
from core.data_manager import Data
from PyQt6.QtCore import Qt
from database.databases import Recipe, Ingredients, Steps
from logic.on_start import construct_string

#---------- АКТИВИРУЕТ РЕЖИМ ПЕРЕТАСКИВАНИЯ ЭЛЕМЕНТОВ QLISTWIDGET
def drag_drop_enable(lw):
    lw.setDragEnabled(True)                          # Включаем перетаскивание
    lw.setAcceptDrops(True)                          # Разрешаем сброс на этот виджет
    lw.setDragDropMode(QListWidget.DragDropMode.InternalMove) # Режим переноса (копирование/перемещение)
    lw.setDropIndicatorShown(True)

# ---------- АКТИВИРУЕТ РЕЖИМ РЕДАКТИРОВАНИЯ ТЕКСТА ЭЛЕМЕНТОВ QLISTWIDGET
def change_list_item(lw):
    index = lw.currentRow()
    item = lw.item(index)
    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

#---------- УДАЛЯЕТ ВЫБРАННЫЙ ЭЛЕМЕНТ ИЗ QLISTWIDGET
def delete_selected_item(lw):
    current_row_index = lw.currentRow()
    if current_row_index >= 0: lw.takeItem(current_row_index)

def delete_item_with_index(lw, index):
    lw.takeItem(index)

# ----------- МЕНЯЕТ ТЕКСТ КОНКРЕТНОГО ЭЛЕМЕНТА
def change_item_text(lw, index: int, recipe: dict):
    item = lw.item(index)
    text = item.text()
    item_number = text[:text.find('.')]
    item.setText(f'{item_number}.{construct_string(recipe)}')

#---------- ВОЗВРАЩАЕТ КОРТЕЖ ИЗ ВСЕХ БАЗ ДАННЫХ
def get_tables() -> tuple[Recipe, Steps, Ingredients]:
    db_path = Data().get_param('db_path')
    return (Recipe(db_path), Steps(db_path), Ingredients(db_path))