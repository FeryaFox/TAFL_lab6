from TAFLCore.BaseInputer import BaseInputer
from TAFLCore.Automate import Automate
from TAFLCore.BaseMenu import BaseMenu


class TAFL5Inputer(BaseInputer):
    def get_alphabet_symbol(self, previous: list[str] | None = None) -> list[str] | None:
        BaseMenu.clear()
        input_phrase = "Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c)(e заразервировано)': \n" \
            if previous is None \
            else f"Введите пожалуйста алфавит входных символов через пробел(пример: 'a b c')(e  заразервировано)(Предыдущий '{' '.join(previous)}'): \n"
        while True:
            alphabet = self._input_alphabet(input_phrase)
            if "e" in alphabet:
                continue
            break
        return alphabet + ["e"]

    def get_alphabet_graph(self, previous: list[str] | None = None) -> list[str] | None:
        input_phrase = "Введите пожалуйста алфавит графа через пробел(пример: 'q0 q1 q2)': \n" \
            if previous is None \
            else f"Введите пожалуйста алфавит графа через пробел(пример: 'q0 q1 q2')(Предыдущий '{' '.join(previous)}'): \n"
        return self._input_alphabet(input_phrase)

    @staticmethod
    def get_input_automate(automate: Automate, is_change_alphabet: bool = False) -> Automate:
        BaseMenu.clear()
        if is_change_alphabet:
            print("Один из начальных алфавитов был заменен, поэтому надо заново задать автомат")
        for state in automate.get_states_alias():
            for signal in automate.get_signals_name():
                print(automate.to_string([{"state_alias": state, "signal_name": signal}]))
                while True:

                    try:
                        print(f"Допустимые состояния: {", ".join(automate.get_all_states())}")
                        input_states = input(f"Введите состояния для ({state}, {signal})(через проблел)(например: 'q0 q1 q2')(или enter для задания пустого): \n").split()
                    except KeyboardInterrupt:
                        return automate

                    if not input_states:
                        print(input_states)

                    if not automate.check_correct_states(input_states):
                        print("Вы ввели состояние, которого нет в автомате")
                        continue
                    automate[state, signal] = input_states
                    BaseMenu.clear()
                    break
        return automate

    @staticmethod
    def get_started_states(automate: Automate) -> Automate:
        BaseMenu.clear()
        print(automate)
        while True:
            try:
                input_states = input(f"Введие начальные вершины (наши состояния {', '.join(automate.get_states_alias())}) через пробел: \n").split()
            except KeyboardInterrupt:
                return automate

            if not input_states:
                print(input_states)
            if not automate.check_correct_states(input_states):
                print("Вы ввели состояние, которого нет в автомате")
                continue

            automate.set_start_state_by_alias(input_states)
            BaseMenu.clear()
            break
        return automate

    @staticmethod
    def get_ended_states(automate: Automate) -> Automate:
        BaseMenu.clear()
        print(automate)
        while True:
            try:
                input_states = input(
                    f"Введие конечные вершины (наши состояния {', '.join(automate.get_states_alias())}) через пробел: \n").split()
            except KeyboardInterrupt:
                return automate

            if not input_states:
                print(input_states)
            if not automate.check_correct_states(input_states):
                print("Вы ввели состояние, которого нет в автомате")
                continue

            automate.set_end_state_by_alias(input_states)
            BaseMenu.clear()
            break
        return automate

    @staticmethod
    def get_word_to_validate(automate: Automate) -> str:
        signals_name = automate.get_signals_name()
        while True:
            correct = True
            word = input("Введите слово для проверки: \n")
            for j in word:
                if j not in signals_name:
                    print("Вы ввели элементы, которые нет в алфавите")
                    correct = False
                    break

            if correct:
                return word

