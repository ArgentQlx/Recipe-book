from database.databases import Recipe, Ingredients, Steps
from core.data_manager import Data

def search_recipes(self):
        query = self.search_input.text().strip()
        if not query: return
        self.search_input.setText('')
        
        recipe_table = Recipe(Data().get_param('db_path'))
        param = Data().get_param('recipe_search_param')
        limit = self.limit_slider.value()
        Data().change_param('results_limit', limit)
        # print(param)

        success, status, results = recipe_table.search_recipes(param, query, limit)
        print(results)
        if not results: return
        self.search_results.clear()
        for recipe in results:
                time = recipe['time_minutes']
                if int(time) - time == 0: time = int(time)
                item_text = f'{recipe['id']}. {recipe['title'].capitalize()} - {time}мин'
                self.search_results.addItem(item_text)

def set_title_param(): Data().change_param('recipe_search_param', 'title')
def set_summary_param(): Data().change_param('recipe_search_param', 'summary')
def set_difficult_param(): Data().change_param('recipe_search_param', 'difficult')

def change_limit_view(self): self.limit_label.setText(f'Ограничить количество результатов: {self.limit_slider.value()}')

def show_all_results_option(self):
        if self.show_all_checkbox.isChecked():
            self.limit_slider.setDisabled(True)
            Data().change_param('results_limit', -1)
            self.limit_label.setText('Ограничить количество результатов: НЕ ОГРАНИЧИВАТЬ')
        else:
            self.limit_slider.setDisabled(False)
            Data().change_param('results_limit', self.limit_slider.value())
            change_limit_view(self)