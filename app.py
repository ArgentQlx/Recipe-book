from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
import sys
from gui.main_window.window import Main_Window
from themes.edit_themes import Themes

def update_user_theme():
    themes = Themes()
    if themes.get_current_theme().lower() != 'пользовательская': return
    themes.set_style(app)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('.\\img\\recipe_logo.png'))
    window = Main_Window()
    window.show()

    Themes().set_style(app)
    window.style_update_btn.clicked.connect(update_user_theme)

    sys.exit(app.exec())
    