from TAFL5.TAFL5Inputer import TAFL5Inputer
from TAFLCore.BaseMenu import BaseMenu


class TAFL6Inputer(TAFL5Inputer):
    def get_alphabet_symbol(self, previous: list[str] | None = None) -> list[str] | None:
        BaseMenu.clear()
        input_phrase = "Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c)': \n" \
            if previous is None \
            else f"Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c')(Предыдущий '{' '.join(previous)}'): \n"
        while True:
            alphabet = self._input_alphabet(input_phrase)
            break
        return alphabet
