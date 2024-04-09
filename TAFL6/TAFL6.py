from TAFLCore.Automate.Automate import Automate, AutomateUtils, TableState


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

                current_table_state = automate.get_table_state_by_alias(i)
                without_unattainable_stated_automate.add_state_row(
                    self.__create_table_state(
                        i,
                        current_table_state.is_start,
                        current_table_state.is_end
                    )
                )
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
