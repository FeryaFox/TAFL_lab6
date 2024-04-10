from TAFLCore.Automate.Automate import Automate, AutomateUtils, TableState
from utils.numberUtils import NumberUtils
import copy


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

    @staticmethod
    def partition_equivalence_classes(automate: Automate) -> list[TableState]:
        equivalence_classes = [
            automate.get_ended_table_state_aliases(),
            automate.get_not_ended_table_state_aliases()
        ]
        num_of_classes = 0
        print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")

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

            num_of_classes += 1
            print(f"Ξ{NumberUtils.covert_number_to_degree(num_of_classes)} = {equivalence_classes}")
            if not flag:
                break

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
