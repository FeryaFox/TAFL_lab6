from TAFLCore.Automate.Automate import Automate, AutomateUtils, TableState, State
from utils.numberUtils import NumberUtils
import copy
import random


class TAFL6:

    def delete_unattainable_stated(self, automate: Automate) -> Automate:

        started_states = automate.get_started_table_state_aliases()

        without_unattainable_stated_automate = Automate(
            states=[self.__create_table_state(started_states[0],
                                              is_start=True,
                                              is_end=False)],
            signals=automate.get_signals_name()
        )
        for i in automate.get_signals_name():
            self.__delete_unattainable_stated(
                automate,
                without_unattainable_stated_automate,
                started_states[0],
                i,
                []
            )
        without_unattainable_stated_automate.sort_table_states()
        return without_unattainable_stated_automate

    def partition_equivalence_classes(
            self,
            automate: Automate
    ) -> list[list[str]]:

        equivalence_classes: list[list[str]] = [
            automate.get_ended_table_state_aliases(),
            automate.get_not_ended_table_state_aliases()
        ]
        num_of_classes = 0
        while True:
            print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
            num_of_classes += 1
            equivalence_classes_old = copy.deepcopy(equivalence_classes)

            temp_classes: dict[int, list[str]] = {}
            for class_num in range(len(equivalence_classes_old)):

                for signal in automate.get_signals_name():
                    temp_classes: dict[int, list[str]] = {}
                    for class_obj in equivalence_classes_old[class_num]:

                        _ = list(automate[class_obj, signal].value)[0]
                        self.__add_equivalence_classes_temp(
                            temp_classes,
                            self.__search_class(equivalence_classes_old, _),
                            class_obj
                        )

                    if len(temp_classes) == 1:
                        continue

                    equivalence_classes[class_num] = []
                    for i in temp_classes:
                        equivalence_classes.append(list(set(temp_classes[i])))

            equivalence_classes = [_ for _ in equivalence_classes if _]

            if equivalence_classes == equivalence_classes_old:
                print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
                return equivalence_classes

    @staticmethod
    def __search_class(
            equivalence_classes: list[list[str]],
            alias: str
    ) -> int:
        for i in range(len(equivalence_classes)):
            for j in equivalence_classes[i]:
                if j == alias:
                    return i

    @staticmethod
    def __add_equivalence_classes_temp(
            classes: dict[int, list[str]],
            class_num: int,
            alias: str
    ) -> dict[int, list[str]]:
        if class_num not in classes:
            classes[class_num] = []
        classes[class_num].append(alias)
        return classes
    @staticmethod
    def create_representatives_automate(
            classes: list[list[str]],
            without_unattainable_stated_automate: Automate
    ) -> Automate:
        representatives = {}
        for i in classes:
            representatives[random.choice(i)] = i

        representatives_automate = Automate(
            states=[],
            signals=without_unattainable_stated_automate.get_signals_name()
        )
        start_state = without_unattainable_stated_automate.get_started_table_state_aliases()[0]
        end_states = without_unattainable_stated_automate.get_ended_table_state_aliases()

        for key, value in representatives.items():
            is_start = False
            is_end = False

            for i in value:
                if i == start_state:
                    is_start = True
                if i in end_states:
                    is_end = True

            _ = AutomateUtils.create_table_state_from_dict(
                {
                    'is_start': is_start,
                    'is_end': is_end,
                    'alias': f"[{key}]",
                    "additional_info": None,
                    "state": value
                }
            )

            representatives_automate.add_state_row(_)

        representatives_automate.sort_table_states()
        for key, value in representatives.items():
            alias = f"[{key}]"
            for signal in without_unattainable_stated_automate.get_signals_name():
                _ = list(without_unattainable_stated_automate[key, signal].value)[0]
                for key_, value_ in representatives.items():
                    if _ in value_:
                        representatives_automate[alias, signal] = [f"[{key_}]"]
        return representatives_automate

    def __delete_unattainable_stated(
            self,
            automate: Automate,
            without_unattainable_stated_automate: Automate,
            current_state: str,
            current_signal: str,
            checked: list[str]
    ) -> None:
        checked.append(current_state)
        if current_state not in without_unattainable_stated_automate.get_states_alias():
            current_table_state = automate.get_table_state_by_alias(current_state)
            without_unattainable_stated_automate.add_state_row(
                self.__create_table_state(
                    current_state,
                    current_table_state.is_start,
                    current_table_state.is_end
                )
            )
        future_state = automate[current_state, current_signal].value

        without_unattainable_stated_automate[current_state, current_signal].append(future_state)

        table_state = without_unattainable_stated_automate.get_states_alias()

        for i in future_state:
            if i == "":
                continue
            if i not in checked:

                # current_table_state = automate.get_table_state_by_alias(i)
                # without_unattainable_stated_automate.add_state_row(
                #     self.__create_table_state(
                #         i,
                #         current_table_state.is_start,
                #         current_table_state.is_end
                #     )
                # )
                for j in automate.get_signals_name():
                    self.__delete_unattainable_stated(
                        automate,
                        without_unattainable_stated_automate,
                        i,
                        j,
                        checked
                    )

    @staticmethod
    def __create_table_state(
            alias: str,
            is_start: bool = False,
            is_end: bool = False
    ) -> TableState:
        return AutomateUtils.create_table_state_from_dict(
            {
                "state": [alias],
                "alias": alias,
                "additional_info": None,
                "is_start": is_start,
                "is_end": is_end
            }
        )
