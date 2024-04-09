import json


class BaseSaver:
    _data: dict
    _filename: str

    def __init__(self, filename: str = "app.json"):
        self.__filename = filename
        self._load_data()

    def _load_data(self):
        try:
            with open(self.__filename, 'r', encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}

    @staticmethod
    def load_decorator(func):
        def wrapper(self, *args, **kwargs):
            self._load_data()
            return func(self, *args, **kwargs)
        return wrapper

    def _save_data(self):
        with open(self.__filename, 'w', encoding="utf-8") as f:
            json.dump(self._data, f)

    @staticmethod
    def save_decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._save_data()
            return result
        return wrapper


