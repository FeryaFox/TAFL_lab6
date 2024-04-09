from .TAFL5Saver import TAFL5Saver
from TAFLCore.Automate import Automate, TableState, AutomateUtils
from typing import TypedDict
from .utils import *


def get_deltas(state: str, signal: str, result: list, automate: Automate, is_signal: bool) -> list:
    if (r := list(automate[state][signal].value)) and not is_signal:
        is_signal = True
        for i in r:
            result.append({
                "state": i,
                "signal": signal,
                "result": []
            })

    if r := list(automate[state]["e"].value):
        for i in r:
            result.append({
                "state": i,
                "signal": "e",
                "result": []
            })

    if len(result) > 0:
        for i in result:
            get_deltas(
                i["state"],
                signal,
                i["result"],
                automate,
                is_signal
            )
    return result


def transform_deltas(input_list):
    result_list = []

    for item in input_list:
        # Функция для сбора состояний и сигналов в рекурсии
        def collect_states_signals(item, states=[], signals=[]):
            states.append(item['state'])
            signals.append(item['signal'])
            for child in item['result']:
                collect_states_signals(child, states, signals)
            return {"states": states, "signals": signals}

        # Используем вспомогательную функцию для каждого элемента
        result = collect_states_signals(item, [], [])
        result_list.append(result)

    return result_list


def filter_signals_states(transformed_list):
    # Удаление словарей, где все сигналы равны 'e'
    new_list = [d for d in transformed_list if not all(signal == 'e' for signal in d['signals'])]

    # Удаление состояний, соответствующих 'e', если после них есть другие сигналы
    for d in new_list:
        e_indices = []
        for i, signal in enumerate(d['signals']):
            if signal == 'e':
                # Если 'e' не последний сигнал или за 'e' следуют не только сигналы 'e'
                if i < len(d['signals']) - 1 and not all(s == 'e' for s in d['signals'][i + 1:]):
                    e_indices.append(i)

        for index in sorted(e_indices, reverse=True):
            del d['states'][index]
            del d['signals'][index]

    return new_list


# Объединение состояний и удаление дубликатов
def combine_unique_states(filtered_list):
    return list(set(state for item in filtered_list for state in item['states']))


class TAFL5:
    @staticmethod
    def construct_e_closures(automate: Automate) -> list[TableState]:
        e_closures: list[TableState] = []
        j = 0

        started_table_states_aliases = automate.get_started_table_state_aliases()

        achievable_started_table_states_aliases = []

        for alias in started_table_states_aliases:
            achievable_started_table_states_aliases.append(alias)
            transitions = automate[alias, "e"].value  # Получаем список переходов для данного алиаса
            if transitions:
                achievable_started_table_states_aliases.extend(transitions)  # Добавляем все переходы в итоговый список

        achievable_started_table_states_aliases = sorted(achievable_started_table_states_aliases)

        for alias in automate.get_states_alias():
            states = list(([alias] + list(automate[alias, "e"].value)))
            states.sort()
            is_start = False
            is_end = False

            for i in achievable_started_table_states_aliases:
                if i in states:
                    is_start = True

            for state in states:
                if automate.get_table_state_by_alias(state).is_end:
                    is_end = True
                    break

            e_closures.append(
                AutomateUtils.create_table_state_from_dict(
                    {
                        "state": states,
                        "alias": f"S{j}",
                        "additional_info": f"Ξ({alias})",
                        "is_start": is_start,
                        "is_end": is_end
                    }
                )
            )
            j += 1
        return e_closures

    @staticmethod
    def get_automaton_transition_table(automate: Automate, e_closures: list[TableState]) -> Automate:
        signals_name = automate.get_signals_name().copy()
        signals_name.remove("e")
        transition_automate = Automate(e_closures, signals_name)

        e_states = []
        s_states = []
        for e_closure in e_closures:

            for signal in transition_automate.get_signals_name():
                e_states = []
                s_states = []
                for state in e_closure.state.value:

                    r = []
                    transformed_list = get_deltas(state, signal, r, automate, False)

                    transformed_list = transform_deltas(transformed_list)
                    filtered_list = filter_signals_states(transformed_list)
                    e_states += combine_unique_states(filtered_list)
                e_states = set(e_states)
                for state in transition_automate.get_states_alias():
                    if e_states in transition_automate.get_table_state_by_alias(state):
                        s_states.append(state)

                transition_automate[e_closure.alias, signal].value = s_states

        return transition_automate

    @staticmethod
    def deparmenize_automate(undeparmenize_automate: Automate) -> Automate:
        started_states = undeparmenize_automate.get_started_table_state_aliases()

        tt = [AutomateUtils.create_table_state_from_dict(
            {
                "state": started_states,
                "alias": "P0",
                "additional_info": None,
                "is_start": True,
                "is_end": False
            }
        )]

        deparmenized_automate_ = Automate(tt, undeparmenize_automate.get_signals_name().copy())

        checked_index = 0
        add_index = 1
        # Пребираем, пока все не пройдет
        while checked_index < deparmenized_automate_.states_count:
            current_state = deparmenized_automate_.get_all_table_states_obj()[checked_index] # получаем текущее состояение из таблицы P
            for signal in deparmenized_automate_.get_signals_name():
                d_final = [] # состояния S
                for i in current_state.state.value:
                    d_final += undeparmenize_automate[i, signal].value

                d_final = set(d_final)
                is_add = False
                if d_final == set():
                    continue
                for i in deparmenized_automate_.get_all_table_states_obj():
                    if d_final == i.state.value:
                        deparmenized_automate_[current_state.alias, signal].value = {i.alias}
                        is_add = True
                        break
                if not is_add:
                    deparmenized_automate_.add_state_row(AutomateUtils.create_table_state_from_dict(
                        {
                            "state": list(d_final),
                            "alias": f"P{add_index}",
                            "additional_info": None,
                            "is_start": False,
                            "is_end": False
                        }
                    ))
                    deparmenized_automate_[current_state.alias, signal].value = {f"P{add_index}"}
                    add_index += 1
            checked_index += 1

        for table_state in deparmenized_automate_.get_all_table_states_obj():
            for state in table_state.state.value:
                if undeparmenize_automate.is_table_state_ended_by_alias(state):
                    table_state.is_end = True

        return deparmenized_automate_

    @staticmethod
    def check_is_valid_word(word: str, automate: Automate):
        next_state = "P0"
        for i in word:
            prev_state = next_state
            next_state = list(automate[next_state, i].value)[0]
            if next_state == "":
                return False

        if automate.get_table_state_by_alias(next_state).is_end:
            return True
        else:
            return False
