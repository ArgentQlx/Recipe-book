import json

class Data():
    def __init__(self):
        self.data_path = '.\\core\\data.json'
        self.data = self.load_data()

    def load_data(self) -> dict:
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f'Ошибка при загрузке данных: {e}')
            return {}

    def change_param(self, param: str, new_value: any):
        if param.lower() not in self.data.keys(): raise ValueError('Такого параметра нет')
        self.data[param.lower()] = new_value
        self.save_data()

    def get_param(self, param: str):
        if param.lower() not in self.data.keys(): raise ValueError('Такого параметра нет')
        return self.data[param]
    
    def save_data(self):
        with open(self.data_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
