import sqlite3
from core.data_manager import Data

class Recipe():
    def __init__(self, db_path: str):
        self.db_path = db_path
        # self.delete_table()
        self.create_table()

    def create_table(self):
        with self.__get_connection() as conn:
            conn.execute('''
                                    CREATE TABLE IF NOT EXISTS recipe(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        title TEXT NOT NULL,
                                        summary TEXT,
                                        time_minutes REAL NOT NULL,
                                        difficult TEXT           
                                    )
    ''')

    def delete_table(self) -> tuple:
        with self.__get_connection() as conn:
            try: 
                conn.execute('''DROP TABLE IF EXISTS recipe''')
                return (True, 'Таблица recipe удалена', None)
            except Exception as e: return (False, f'Ошибка при удалении таблицы: {e}', None)

    def get_all_recipes(self) -> list:
        with self.__get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM recipe''')
            return [dict(row) for row in cursor.fetchall()]
        
    def search_recipes(self, param: str, search_query: str, limit: int) -> tuple:
        with self.__get_connection() as conn:
            cursor = conn.execute(f'''SELECT * FROM recipe WHERE {param} LIKE ? LIMIT ?''', (f'%{search_query}%', limit))
            # cursor = conn.execute(f'''SELECT * FROM recipe WHERE {param} LIKE %{search_query}%''')
            result = [dict(row) for row in cursor.fetchall()]
            return (True, 'Найден рецепт по айди', result) if result else (False, 'Ничего не найдено', None)


    def get_recipe(self, id: int):
        with self.__get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM recipe WHERE id = (?)''', (id,))
            result = cursor.fetchone()
            return (True, 'Найден рецепт по айди', dict(result)) if result else (False, 'Ничего не найдено', None)

    def add_recipe(self, title: str, summary: str, time: float, difficult: str) -> tuple:
        '''возвращает кортеж (успех, сообщение, данные)'''
        with self.__get_connection() as conn:
            # if difficult.lower() not in ('легкий', 'средний', 'тяжелый'):
            #     return (False, 'Неправильное значение для сложности рецепта: легкий/средний/тяжелый', None)
            try:
                cursor = conn.execute('''INSERT INTO recipe (title, summary, time_minutes, difficult) VALUES (?, ?, ?, ?)''', (title, summary, time, difficult))
                return (True, 'Рецепт добавлен', cursor.lastrowid)
            except Exception as e: 
                return (False, f'Ошибка при добавлении рецепта: {e}', None)
            
    def update_recipe(self, id: int, title: str, summary: str, time_minutes: float, difficult: str) -> tuple:
        if difficult.lower() not in [None, 'легкий', 'средний', 'тяжелый']:
                return (False, 'Неправильное значение для сложности рецепта: легкий/средний/тяжелый', None)
        clause, values = [], []
        if title is not None and title:
            clause.append('title = ?')
            values.append(title)
        if summary is not None:
            clause.append('summary = ?')
            values.append(summary)
        if time_minutes is not None:
            clause.append('time_minutes = ?')
            values.append(time_minutes)
        if difficult is not None:
            clause.append('difficult = ?')
            values.append(difficult)
        with self.__get_connection() as conn:
            try:
                conn.execute(f'''UPDATE recipe SET {', '.join(clause)} WHERE id = (?)''', (*values, id))
                return (True, f'Заменены поля: {values}', id)
            except Exception as e:
                return (False, f'Ошибка при замене данных рецепта: {e}', id)

    def remove_recipe(self, id: int) -> tuple:
        '''удаляет рецепт по айди'''
        with self.__get_connection() as conn:
            try:
                conn.execute('''DELETE FROM recipe WHERE id = (?)''', (id,))
                return (True, f'Рецепт с id {id} удален', id)
            except Exception as e: 
                return (False, f'Ошибка при удалении рецепта: {e}', None)

    def __get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
    
class Steps():
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with self.__get_connection() as conn:
            conn.execute('PRAGMA foreign_keys = ON;')
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS step(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            step_text TEXT NOT NULL,
                            step_number INTEGER NOT NULL,
                            recipe_id INTEGER NOT NULL,
                            FOREIGN KEY (recipe_id) REFERENCES recipe (id) ON DELETE CASCADE
                            )
            ''')

    def delete_table(self) -> tuple:
        with self.__get_connection() as conn:
            try:
                conn.execute('''DROP TABLE IF EXISTS step''')
                return (True, 'Таблица step удалена', None)
            except Exception as e: return (False, f'Ошибка при удалении таблицы: {e}', None)

    def add_step(self, text: str, step_number: int, recipe_id: int) -> tuple:
        if step_number <= 0: raise 'Номер шага не может быть <= 0'
        with self.__get_connection() as conn:
            try:
                cursor = conn.execute('''INSERT INTO step (step_text, step_number, recipe_id) VALUES (?, ?, ?)''', (text, step_number, recipe_id))
                return (True, 'Шаг рецепта добавлен', cursor.lastrowid)
            except Exception as e: return (False, f'Ошибка при добавлении шага: {e}', None)

    def update_step(self, step_id: int, text: str, step_number: int) -> tuple:
        clauses, values = [], []
        if text not in [None, '']:
            clauses.append('step_text = ?')
            values.append(text)
        if step_number is not None:
            clauses.append('step_number = ?')
            values.append(step_number)
        with self.__get_connection() as conn:
            try:
                conn.execute(f'''UPDATE step SET {', '.join(clauses)} WHERE id = ?''', (*values, step_id))
                return (True, f'Заменены поля: {values}', None)
            except Exception as e: return (False, f'Ошибка при замене поля в step: {e}', None)
        
    def remove_steps(self, recipe_id: int) -> tuple:
        with self.__get_connection() as conn:
            try:
                conn.execute('''DELETE FROM step WHERE recipe_id = (?)''', (recipe_id,))
                return (True, f'Шаги рецепта с id {recipe_id} удалены', recipe_id)
            except Exception as e: 
                return (False, f'Ошибка при удалении шага рецепта: {e}', None)
            
    def count_steps(self, recipe_id: int) -> int:
        with self.__get_connection() as conn:
            cursor = conn.execute('''SELECT COUNT(*) FROM step WHERE recipe_id = ?''', (recipe_id,))
            return (True, 'Количество шагов в рецепте', cursor.fetchone()[0])

    def get_steps(self, recipe_id: int) -> list:
        with self.__get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM step WHERE recipe_id = ?''', (recipe_id,))
            result = cursor.fetchall()
            return [dict(row) for row in result] if result else None 

    def __get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
    
class Ingredients():
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        with self.__get_connection() as conn:

            conn.execute('''
                        CREATE TABLE IF NOT EXISTS ingredient (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            unit TEXT NOT NULL,
                            amount INTEGER NOT NULL,
                            recipe_id INTEGER NOT NULL,
                            FOREIGN KEY (recipe_id) REFERENCES recipe (id) ON DELETE CASCADE
                        )
            ''')

    def delete_table(self) -> tuple:
        with self.__get_connection() as conn:
            try:
                conn.execute('''DROP ingredient IF EXISTS''')
                return (True, 'Таблица ingredient удалена', None)
            except Exception as e: return (False, f'Ошибка при удалении ingredient: {e}', None)

    def add_ingredient(self, name: str, unit: str, amount: int, recipe_id: int) -> tuple:
        with self.__get_connection() as conn:
            try:
                cursor = conn.execute('''INSERT INTO ingredient (name, unit, amount, recipe_id) VALUES (?, ?, ?, ?)''', (name, unit, amount, recipe_id))
                return (True, 'Ингредиент добавлен', cursor.lastrowid)
            except Exception as e: return (False, f'Ошибка при добавлении ингредиента: {e}', None)

    def remove_ingredients(self, recipe_id: int) -> tuple:
        with self.__get_connection() as conn:
            try:
                cursor = conn.execute('''DELETE FROM ingredient WHERE recipe_id = (?)''', (recipe_id,))
                return (True, 'Игредиенты удалены', cursor.lastrowid)
            except Exception as e: return (False, f'Ошибка при удалении ингредиента: {e}', None)

    def count_ingreditnts(self, recipe_id: int) -> tuple:
        with self.__get_connection() as conn:
            try:
                cursor = conn.execute('''SELECT COUNT(*) FROM ingredient WHERE recipe_id = (?)''', (recipe_id,))
                return (True, 'Количество ингредиентов в рецепте', cursor.fetchone()[0])
            except Exception as e: return (False, f'Ошибка при подсчете ингредиентов: {e}', None)

    def get_ingredients(self, recipe_id: int) -> list:
        with self.__get_connection() as conn:
            cursor = conn.execute('''SELECT * FROM ingredient WHERE recipe_id = ?''', (recipe_id,))
            result = cursor.fetchall()
            return [dict(row) for row in result] if result else None

    def __get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
    