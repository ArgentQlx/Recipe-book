from PyQt6.QtCore import QTime
from logic.on_start import load_all_recipes
from logic.some_events import get_tables

#---------- ДОСТАЕТ ИЗ СЫРОЙ СТРОКИ СПИСКА ИНГРЕДИЕНТОВ ЗНАЧЕНИЯ
def parse_ingredient_list(text: str):
       name, amount, unit = text.split()
       return (name[:-1], int(amount), unit[1:-1])

#---------- ДОБАВЛЯЕТ ИНГРЕДИЕНТ В СПИСОК ИНГРЕДИЕНТОВ РЕЦЕПТА (ДОБАВЛЕНИЕ)
def write_ingredient(self):
        title = self.ingredient_title_input.text()
        unit = self.ingredient_unit_input.text()
        amount = int(self.ingredient_amount.text())
        if not title or not unit: return

        self.ingredient_title_input.setText('')
        self.ingredient_unit_input.setText('')
        self.ingredient_amount.setValue(1)
        
        self.ingredients_list.addItem(f'{title.strip().capitalize().replace(' ', '_')}: {amount} [{unit.strip().replace(' ', '_')}]')

#---------- ДОБАВЛЯЕТ ШАГ В СПИСОК ШАГ РЕЦЕПТА (ДОБАВЛЕНИЕ)
def write_step(self):
        text = self.step_summary_input.toPlainText()
        if not text: return
        self.steps_list.addItem(text)

        self.step_summary_input.setText('')

#---------- ДОБАВЛЯЕТ РЕЦЕПТ В БАЗУ ДАННЫХ (ПЕРВОЕ ДОБАВЛЕНИЕ)
def add_recipe(self):
       recipe_title = self.recipe_title_input.text()
       recipe_summary = self.recipe_summary_input.toPlainText()
       time_minutes = self.recipe_time_input.time().hour() * 60 + self.recipe_time_input.time().minute()
       difficult = self.recipe_difficult.currentText()

       if not recipe_title: return

       steps = [self.steps_list.item(i).text() for i in range(self.steps_list.count())]
       ingredients = [self.ingredients_list.item(i).text() for i in range(self.ingredients_list.count())]
       if not steps or not ingredients: return

       recipe_table, steps_table, ingredients_table = get_tables()

       status = recipe_table.add_recipe(recipe_title, recipe_summary, time_minutes, difficult)
       print(status)
       if not status[0]:
              print(status[1])
              return
       print(status[1])

       self.recipe_title_input.setText('')
       self.recipe_summary_input.setText('')
       self.recipe_time_input.setTime(QTime(0, 0, 0))
       self.steps_list.clear()
       self.ingredients_list.clear()

       for step_number, step_text in enumerate(steps, start=1):
              steps_table.add_step(step_text, step_number, status[-1])
       for ingredient in ingredients:
              name, amount, unit = parse_ingredient_list(ingredient)
              ingredients_table.add_ingredient(name, unit, amount, status[-1])
       load_all_recipes(self.all_recipes_list)