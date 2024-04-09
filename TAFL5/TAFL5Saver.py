from TAFLCore.BaseSaver import BaseSaver
from TAFLCore.Automate.Automate import AutomateDict

class TAFL5Saver(BaseSaver):

    def __init__(self):
        super().__init__()

    @BaseSaver.load_decorator
    def load_data(self) -> dict:
        return self._data

    @BaseSaver.load_decorator
    def load_alphabet_symbol(self) -> list[str] | None:
        try:
            return self._data["alphabet_symbol"]
        except KeyError:
            return None

    @BaseSaver.save_decorator
    def save_alphabet_symbol(self, alphabet_symbol: list[str]) -> None:
        self._data["alphabet_symbol"] = alphabet_symbol

    @BaseSaver.load_decorator
    def load_alphabet_graph(self) -> list[str] | None:
        try:
            return self._data["alphabet_graph"]
        except KeyError:
            return None

    @BaseSaver.save_decorator
    def save_alphabet_graph(self, alphabet_graph: list[str]) -> None:
        self._data["alphabet_graph"] = alphabet_graph

    @BaseSaver.load_decorator
    def load_input_automate(self) -> AutomateDict:
        return self._data["input_automate"]

    @BaseSaver.save_decorator
    def save_input_automate(self, input_automate: AutomateDict) -> None:
        self._data["input_automate"] = input_automate

    def save_all(self, alphabet_symbol: list[str], alphabet_graph: list[str], input_automate: AutomateDict) -> None:
        self.save_alphabet_symbol(alphabet_symbol)
        self.save_alphabet_graph(alphabet_graph)
        self.save_input_automate(input_automate)
