from gui.recipe_window.recipe_window_gui import Ui_Dialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal
from logic.some_events import drag_drop_enable, get_tables, change_list_item, delete_selected_item
from logic.edit_recipe import save_recipe, set_recipe_edit, set_recipe_info
from gui.dialog_window import ModalWindow
from themes.edit_themes import Themes

class Recipe_Window(QDialog, Ui_Dialog):
    del_confirm_signal = pyqtSignal()

    def __init__(self, recipe_id: int, signal, reopen_signal, item_index: int):
        self.recipe_id = recipe_id
        super().__init__()

        self.modal = 0
        self.item_index = item_index
        self.signal = signal # для изменения списка всех рецептов в главном окне
        self.reopen_signal = reopen_signal # для переоткрыия окна после редактирования рецепта
        recipe_tb, steps_tb, ingred_tb = get_tables()

        self.recipe = recipe_tb.get_recipe(self.recipe_id)[-1]
        self.steps = steps_tb.get_steps(self.recipe_id)
        self.ingredients = ingred_tb.get_ingredients(self.recipe_id)

        self.setupUi(self)
        self.steps_list.setProperty('class', 'recipe_widget')
        self.init_events()

        set_recipe_info(self)
        set_recipe_edit(self)
        Themes().set_style(self)
        self.tabWidget.setCurrentIndex(0)
        self.show()

    #---------- ИНИЦИАЛИЗАЦИЯ СОБЫТИЙ
    def init_events(self):
        for lw in (self.steps_edit, self.ingredients_edit): drag_drop_enable(lw)

        self.steps_edit.itemDoubleClicked.connect(lambda: change_list_item(self.steps_edit))
        self.ingredients_edit.itemDoubleClicked.connect(lambda: change_list_item(self.ingredients_edit))
        self.del_steps_btn.clicked.connect(lambda: delete_selected_item(self.steps_edit))
        self.del_ingredients_btn.clicked.connect(lambda: delete_selected_item(self.ingredients_edit))
        self.save_recipe_btn.clicked.connect(lambda: save_recipe(self))
        self.del_recipe_btn.clicked.connect(lambda: self.confirm_delete())

        self.steps_edit.setProperty('class', 'recipe_widget')
        self.ingredients_edit.setProperty('class', 'recipe_widget')

        self.del_confirm_signal.connect(self.delete_recipe)

    #---------- УДАЛЕНИЕ РЕЦЕПТА
    def delete_recipe(self):

        recipe_tb, steps_tb, ingred_tb = get_tables()
        print(recipe_tb.remove_recipe(self.recipe_id))
        print(steps_tb.remove_steps(self.recipe_id))
        print(ingred_tb.remove_ingredients(self.recipe_id))
        self.signal.emit(0, {}, 1)
        if not self.modal: self.modal.close()
        self.close()

    def confirm_delete(self):
        self.modal = ModalWindow('Вы точно хотите удалить этот рецепт?', self.del_confirm_signal)

                
