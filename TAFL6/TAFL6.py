from TAFLCore.Automate.Automate import Automate, AutomateUtils, TableState, State
from utils.numberUtils import NumberUtils
import copy
from dataclasses import dataclass


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

    def partition_equivalence_classes_(
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
            equivalence_classes = []
            temp_classes: dict[int, list[str]] = {}
            for class_num in range(len(equivalence_classes_old)):
                temp_classes: dict[int, list[str]] = {}
                for class_obj in equivalence_classes_old[class_num]:
                    for signal in automate.get_signals_name():
                        _ = list(automate[class_obj, signal].value)[0]
                        self.__add_equivalence_classes_temp(
                            temp_classes,
                            self.__search_class(equivalence_classes_old, _),
                            class_obj
                        )


                count_dict = {}

                for key, value in temp_classes.items():

                    temp_dict = {}
                    for item in value:
                        if item in temp_dict:
                            temp_dict[item] += 1
                        else:
                            temp_dict[item] = 1

                    count_dict[key] = temp_dict

                print(count_dict)
                aa = []
                for key, value in count_dict.items():
                    for key1, value1 in value.items():
                        if value1 == 2:
                            aa.append(key1)

                for i in aa:
                    for key, value in temp_classes.items():
                        try:
                            value.remove(i)
                            value.remove(i)
                        except (ValueError, KeyError):
                            pass
                for i in temp_classes:
                    if i != num_of_classes:
                        for j in temp_classes[i]:
                            try:
                                temp_classes[num_of_classes].remove(j)
                            except (ValueError, KeyError):
                                pass
                for i in temp_classes:
                    equivalence_classes.append(list(set(temp_classes[i])))
                equivalence_classes.append([_ for _ in aa])

            equivalence_classes = [_ for _ in equivalence_classes if _]

            if equivalence_classes == equivalence_classes_old:
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
    def partition_equivalence_classes(automate: Automate):
        # @dataclass
        # class Temp:
        #     state_alias: str
        #     signal: str
        #     equivalence_class: int
        #
        # equivalence_classes: dict[int, list[str]] = {
        #     1: automate.get_ended_table_state_aliases(),
        #     2: automate.get_not_ended_table_state_aliases()
        # }
        # num_of_classes = 0
        # print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
        #
        # temp: dict[int, list[Temp]] = {}
        #
        # while True:
        #     for i in equivalence_classes:
        #         for j in equivalence_classes[i]:
        #             for k in automate.get_signals_name():
        #                 _ = list(automate[j, k].value)[0]
        #                 for ii in equivalence_classes:
        #                     for jj in equivalence_classes[ii]:
        #                         if jj == _:
        #                             if i not in temp:
        #                                 temp[i] = []
        #                             temp[i].append(
        #                                 Temp(
        #                                     j,
        #                                     k,
        #                                     ii
        #                                 )
        #                             )
        #     import pprint
        #     pprint.pprint(temp)
        #
        #     for i in temp:
        #         for j in temp[i]:
        #            ...
        #
        #     break
        equivalence_classes: list[list[str]] = [
            automate.get_ended_table_state_aliases(),
            automate.get_not_ended_table_state_aliases()
        ]
        num_of_classes = 0
        # print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
        while True:
            flag = False
            old_equivalence_classes = copy.deepcopy(equivalence_classes)
            for i in range(len(old_equivalence_classes)):
                new_equivalence_classes = []
                for j in old_equivalence_classes[i]:
                    for k in automate.get_signals_name():
                        _ = list(automate[j, k].value)[0]
                        if _ == "":
                            continue

                        if _ not in old_equivalence_classes[i] and j not in new_equivalence_classes:
                            flag = True
                            new_equivalence_classes.append(j)
                if new_equivalence_classes:
                    if new_equivalence_classes == old_equivalence_classes[i]:
                        flag = False
                    else:
                        for j in new_equivalence_classes:
                            equivalence_classes[i].remove(j)
                        equivalence_classes.append(new_equivalence_classes)
                        # for j in new_equivalence_classes:
                        #     equivalence_classes[i].remove(j)
                        #     equivalence_classes.append([j])

            num_of_classes += 1
            # print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
            if not flag:
                break
        return equivalence_classes

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
