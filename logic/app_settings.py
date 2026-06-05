import subprocess
from core.data_manager import Data

def open_style_file():
    path = Data().get_param('themes')['Пользовательская']
    subprocess.Popen(['notepad.exe', path])

def open_json_file():
    path = '.\\core\\data.json'
    subprocess.Popen(['notepad.exe', path])

