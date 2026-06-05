from PyQt6.QtWidgets import QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import QTime
from logic.add_recipe import parse_ingredient_list
from logic.some_events import get_tables

#---------- УСТАНАВЛИВАЕТ ИНФОРМАЦИЮ О РЕЦЕПТЕ ДЛЯ ПРОСМОТРА ПРИ СОЗДАНИИ ОКНА
def set_recipe_info(self):
        self.steps_list.clear()
        self.ingredients_view.clearContents()

        self.setWindowTitle(self.recipe['title'])
        self.title_label.setText(self.recipe['title'])
        self.summary_label.setText(self.recipe['summary'])

        time = self.recipe['time_minutes']
        if int(time) - time == 0: time = int(time)
        self.time_label.setText(f'Время готовки: {time}мин.')

        for step in self.steps:
            self.steps_list.addItem(f'{step['step_number']}. {step['step_text']}')

        # self.ingredients_view = QTableWidget(len(ingredients[0].keys()), 3)
        self.ingredients_view.setRowCount(len(self.ingredients))
        self.ingredients_view.verticalHeader().setVisible(False)
        self.ingredients_view.setColumnCount(3)
        self.ingredients_view.setHorizontalHeaderLabels(['Название', 'Количество', 'Единица измерения'])
        for row, ingredient in enumerate(self.ingredients):
            self.ingredients_view.setItem(row, 0, QTableWidgetItem(ingredient['name'].replace('_', ' ')))
            self.ingredients_view.setItem(row, 1, QTableWidgetItem(str(ingredient['amount'])))
            self.ingredients_view.setItem(row, 2, QTableWidgetItem(ingredient['unit'].replace('_', ' ')))
        self.ingredients_view.resizeColumnsToContents()
        self.ingredients_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ingredients_view.horizontalHeader().setStretchLastSection(True)

#---------- ОТОБРАЖАЕТ ИНФОРМАЦИЮ О РЕЦЕПТЕ ВО ВЛАДКЕ ЕГО РЕДАКТИРОВАНИЯ
def set_recipe_edit(self):
        self.title_edit.setText(self.recipe['title'])
        self.summary_edit.setText(self.recipe['summary'])
        self.difficult_edit.setCurrentText(self.recipe['difficult'])
        hh = self.recipe['time_minutes'] // 60
        mm = self.recipe['time_minutes'] - hh * 60
        self.time_edit.setTime(QTime(int(hh), int(mm), 0))

        for step in self.steps: self.steps_edit.addItem(step['step_text'])
        for ingredient in self.ingredients: self.ingredients_edit.addItem(f'{ingredient['name'].strip().capitalize().replace(' ', '_')}: {ingredient['amount']} [{ingredient['unit'].strip().replace(' ', '_')}]')

#---------- СОХРАНЯЕТ РЕДАКТИРОВАННЫЙ РЕЦЕПТ В БАЗУ ДАННЫХ
def save_recipe(self):
        title = self.title_edit.text()
        if not title: return
        summary = self.summary_edit.toPlainText()
        time = self.time_edit.time().hour() * 60 + self.time_edit.time().minute()
        difficult = self.difficult_edit.currentText()

        recipe_table, steps_table, ingredients_table = get_tables()

        status = recipe_table.update_recipe(self.recipe_id, title, summary, time, difficult)
        if not status[0]: return

        steps = [self.steps_edit.item(i).text() for i in range(self.steps_edit.count())]
        ingredients = [self.ingredients_edit.item(i).text() for i in range(self.ingredients_edit.count())]
        if not steps or not ingredients: return

        steps_table.remove_steps(self.recipe_id)
        ingredients_table.remove_ingredients(self.recipe_id)

        for step_number, step_text in enumerate(steps, start=1):
               steps_table.add_step(step_text, step_number, self.recipe_id)
        for ingredient in ingredients:
               name, amount, unit = parse_ingredient_list(ingredient)
               ingredients_table.add_ingredient(name, unit, amount, self.recipe_id)
        
        self.recipe = get_tables()[0].get_recipe(self.recipe_id)[-1]
        self.reopen_signal.emit(self.recipe_id)
        self.signal.emit(self.item_index, self.recipe, 0)