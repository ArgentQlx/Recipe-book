# from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from gui.main_window.window_gui import Ui_MainWindow
from logic.add_recipe import write_ingredient, write_step, add_recipe
from logic.search_recipe import search_recipes, set_title_param, set_summary_param, set_difficult_param, change_limit_view, show_all_results_option
from logic.on_start import restore_window_data, load_all_recipes
from logic.some_events import delete_selected_item, drag_drop_enable, change_list_item, change_item_text
from core.data_manager import Data
from logic.app_settings import open_style_file, open_json_file
from gui.recipe_window.recipe_window import Recipe_Window
from themes.edit_themes import Themes

class Main_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    recipe_update_signal = pyqtSignal(int, dict, int) # меняет all_recipe_list при изменении рецепта в другом окне
    reopen_window_signal = pyqtSignal(int) # переоткрывает окно после редактирования рецепта

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Книга рецептов')
        self.init_events()
        self.recipe_window = 0
        restore_window_data(self)
        load_all_recipes(self.all_recipes_list)
        self.resize(800, 800)
        self.tabWidget.setCurrentIndex(0)
        self.textBrowser_3.setOpenExternalLinks(True)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        Themes().set_themes_titles(self.themes_list)

    #---------- ИНИЦИАЛИЗАЦИЯ СОБЫТИЙ
    def init_events(self):
        self.steps_list.setProperty('class', 'recipe_widget')
        self.ingredients_list.setProperty('class', 'recipe_widget')
        self.steps_list.itemDoubleClicked.connect(lambda: change_list_item(self.steps_list))
        self.ingredients_list.itemDoubleClicked.connect(lambda: change_list_item(self.ingredients_list))
        drag_drop_enable(self.steps_list)
        drag_drop_enable(self.ingredients_list)

        self.add_ingredient_btn.clicked.connect(lambda: write_ingredient(self))
        self.add_step_btn.clicked.connect(lambda: write_step(self))
        self.add_recipe_btn.clicked.connect(lambda: add_recipe(self))
        self.del_step_btn.clicked.connect(lambda: delete_selected_item(self.steps_list))
        self.del_ingredient_btn.clicked.connect(lambda: delete_selected_item(self.ingredients_list))

        self.search_btn.clicked.connect(lambda: search_recipes(self))
        self.search_input.returnPressed.connect(lambda: search_recipes(self))
        self.title_param.toggled.connect(set_title_param)
        self.summary_param.toggled.connect(set_summary_param)
        self.difficult_param.toggled.connect(set_difficult_param)

        self.open_style_btn.clicked.connect(open_style_file)
        self.open_json_btn.clicked.connect(open_json_file)

        self.recipe_update_signal.connect(self.change_all_recipes_list)
        self.reopen_window_signal.connect(self.reopen_window)

        self.limit_slider.valueChanged.connect(lambda: change_limit_view(self))
        self.show_all_checkbox.clicked.connect(lambda: show_all_results_option(self))

        self.all_recipes_list.doubleClicked.connect(self.show_recipe)
        self.search_results.doubleClicked.connect(self.show_recipe)

        self.themes_list.currentIndexChanged.connect(lambda: Themes().change_theme(self.themes_list.currentText(), self))

    #---------- СОХРАНЕНИЕ НЕКОТОРЫХ ДАННЫХ ПРИ ЗАКРЫТИИ ОКНА
    def closeEvent(self, event):
        Data().change_param('results_limit', self.limit_slider.value())
        if self.recipe_window: self.recipe_window.close()

    #---------- ОТОБРАЖАЕТ ВЫБРАННЫЙ ИЗ СПИСКА РЕЦЕПТ В НОВОМ ОКНЕ
    def show_recipe(self):
        item = self.sender().currentItem().text()
        recipe_id = int(item[item.rfind('(', -10) + 1:-1])

        self.recipe_window = Recipe_Window(recipe_id, self.recipe_update_signal, self.reopen_window_signal, self.sender().currentRow())
    
    # ---------- ПЕРЕСОЗДАЕТ ОКНО ПОСЛЕ РЕДАКТИРОВАНИЯ РЕЦЕПТА
    def reopen_window(self, recipe_id: int):
        self.recipe_window.close()
        self.recipe_window = Recipe_Window(recipe_id, self.recipe_update_signal, self.reopen_window_signal, self.all_recipes_list.currentRow())

    # ---------- ФУНКЦИЯ ПОДОГНАННАЯ ПОД КОНКРЕТНЫЙ ЭЛЕМЕНТ
    def change_all_recipes_list(self, index, recipe, status):
        # status 0: рецепт изменен, 1: рецепт удален. Обновление списка всех рецептов
        match status:
            case 0: change_item_text(self.all_recipes_list, index, recipe)
            case 1: load_all_recipes(self.all_recipes_list)


