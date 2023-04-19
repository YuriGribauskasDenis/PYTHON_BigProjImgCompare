from pathlib import Path
from datetime import datetime

def gen_timename():
    return datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

def get_folder_adr(file):
    return Path(file).resolve().parent

def get_file_adr(file):
    return Path(file).resolve()

def get_file_number(file):
    return len([child for child in Path(file).iterdir()])