from core.data_manager import Data
from logic.search_recipe import show_all_results_option
from database.databases import Recipe

# ---------- СОБИРАЕТ НЕКОТОРЫЕ ДАННЫЕ РЕЦЕПТА В ФОРМАТИРОВАННУЮ СТРОКУ
def construct_string(recipe: dict) -> str:
    time = recipe['time_minutes']
    if int(time) - time == 0: time = int(time)
    summary = recipe['summary'].capitalize()
    if len(summary) < 70: summary += '...' + (' ' * (70 - len(summary)))
    else: summary = summary[:67] + '...'
    title = recipe['title'].capitalize()
    if len(title) < 20: title += '.' + (' ' * (20 - len(title)))
    else: title = title[:17] + '...'
    
    return f'{title}{' ' * 10}{summary}{' ' * 10}{time}мин   id({recipe['id']})'

# ---------- ВОССТАНАВЛИВАЕТ ДАННЫЕ ИЗ ФАЙЛА 
def restore_window_data(self):
        data_manager = Data()
        limit = data_manager.get_param('results_limit')
        search_param = data_manager.get_param('recipe_search_param')

        self.limit_slider.setValue(limit)
        if limit == -1:
            self.show_all_checkbox.click()
            show_all_results_option(self)

        match search_param:
            case 'title': self.title_param.click()
            case 'summary': self.summary_param.click()
            case 'difficult': self.difficult_param.click()

# ---------- ОТОБРАЖАЕТ СПИСОК ВСЕХ РЕЦЕПТОВ ПРИ СОЗДАНИИ ОКНА (И ОБНОВЛЯЕТ)
def load_all_recipes(lw):
        lw.clear()
        data_manager = Data()
        all_recipes = Recipe(data_manager.get_param('db_path')).get_all_recipes()
        for index, recipe in enumerate(all_recipes, start=1):
            
            lw.addItem(f'{index}. {construct_string(recipe)}')

