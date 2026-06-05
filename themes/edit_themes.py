from core.data_manager import Data

class Themes():
    def __init__(self):
        self.data = Data()
        self.themes = self.data.get_param('themes')
        self.current_theme = self.data.get_param('current_theme')

    def get_current_theme(self): return self.current_theme

# ---------- УСТАНАВЛИВАЕТ НАЗВАНИЯ ТЕМ В QCOMBOBOX ДЛЯ ИХ ВЫБОРА
    def set_themes_titles(self, cb):
        cb.clear()
        cb.addItems(self.themes.keys())
        cb.setCurrentText(self.current_theme)

# ---------- ПРИМЕНЯЕТ СТИЛИ К ПЕРЕДАННОМУ ВИДЖЕТУ
    def set_style(self, widget):
        with open(self.themes[self.current_theme], 'r', encoding='utf-8') as style:
            widget.setStyleSheet("")
            widget.setStyleSheet(style.read())

# ---------- МЕНЯЕТ ТЕМУ И СРАЗУ ЖЕ ПРИМЕНЯЕТ ЕЕ + СОХРАНЯЕТ
    def change_theme(self, new_theme, widget):
        if new_theme not in self.themes.keys(): return
        self.current_theme = new_theme
        self.set_style(widget)
        self.data.change_param('current_theme', self.current_theme)

