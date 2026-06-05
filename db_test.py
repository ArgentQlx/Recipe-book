from database.databases import Recipe, Steps, Ingredients
from core.data_manager import Data

db_path = Data().get_param('db_path')

# ТЕСТ РЕЦЕПТОВ
table = Recipe(db_path)
# print(table.add_recipe('картошка', 'вкусная, горячая, белорусская', 2.0, 'легкий'))
# print(table.add_recipe('картошка', 'вкусная, горячая, белорусская', 2.0, 'легкий'))
# print(table.get_recipe(1))
# print(table.update_recipe(1, 'Картошечка', None, None, None))
# print(table.get_recipe(1))
# print(table.get_all_recipes())

# # # ТЕСТ ШАГОВ РЕЦЕПТА
# steps = Steps(db_path)

# # # print(steps.add_step('почистить картошку', 1, 1))
# # # print(steps.add_step('нарезать полосками', 2, 1))
# # # print(steps.add_step('обжарить', 3, 1))
# # # print(steps.add_step('посолить', 4, 1))
# # # print(steps.add_step('подать к столу', 5, 1))

# print(steps.get_steps(1))
# print(steps.count_steps(1))

# # # ТЕСТ ИНГРЕДИЕНТОВ
# ingredients = Ingredients(db_path)
# # # # print(ingredients.add_ingredient('вода', "литр", 1, 1))
# # # # print(ingredients.add_ingredient('картофель', "шт", 15, 1))
# # # # print(ingredients.add_ingredient('соль', "столовая ложка", 2, 1))
# print(ingredients.get_ingredients(2))
# print(ingredients.count_ingreditnts(2))

# print(isinstance(10.0, int))

print('(     ))()'.rfind('(', -3))