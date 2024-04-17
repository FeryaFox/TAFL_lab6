from dataclasses import dataclass
from prettytable import PrettyTable
from typing import TypedDict


class TableStateDict(TypedDict):
    state: list[str]
    alias: str
    additional_info: str | None
    is_start: bool
    is_end: bool


class AutomateDict(TypedDict):
    table_states: list[TableStateDict]
    table_signals: list[str]
    states: list[list[list[str]]]


class StateDict(TypedDict):
    state_alias: str
    signal_name: str


@dataclass
class State:
    value: set[str]

    def __str__(self) -> str:
        if len(self.value) == 0 or (len(self.value) == 1 and str(next(iter(self.value))) == ""):
            return "Ø"
        return f"{', '.join(sorted(self.value))}"

    def __contains__(self, item: list[str] | set[str] | str) -> bool:
        if isinstance(item, str):
            return item in self.value
        return self.value.issubset(set(item))

    def append(self, item: set[str] | str) -> None:
        if isinstance(item, str):
            if self.value == {""}:
                self.value = set(item)
                return
            self.value.add(item)
        elif isinstance(item, set):
            if self.value == {""}:
                self.value = item
                return
            self.value |= item

@dataclass
class TableState:

    state: State
    alias: str
    additional_info: str | None = None

    is_start: bool = False
    is_end: bool = False

    def __str__(self) -> str:

        string_automate = ""
        states = ", ".join(sorted(self.state.value))
        if self.alias is not None and self.additional_info is not None:
            string_automate += f"{self.alias} = {self.additional_info} = {{ {states} }}"
        elif self.alias is None and self.additional_info is not None:
            string_automate += f"{self.additional_info} = {{ {states} }}"
        elif self.alias is not None and self.additional_info is None:
            string_automate += f"{self.alias} = {{ {states} }}"
        elif self.alias is None and self.additional_info is None:
            string_automate += f"{{ {states} }}"
        if self.is_end:
            string_automate = "[ " + string_automate + " ]"
        if self.is_start:
            string_automate = "-> " + string_automate

        return string_automate

    def __contains__(self, item: list[str] | State) -> bool:
        item_ = item
        if isinstance(item, State):
            item_ = item.value
        return self.state.value.issubset(set(item_))

    def to_string_ignore_is_start_or_end(self) -> str:

        if self.alias is not None and self.additional_info is not None:
            return f"{self.alias} = {self.additional_info} = {{ {str(self.state)} }}"
        elif self.alias is None and self.additional_info is not None:
            return f"{self.additional_info} = {{ {str(self.state)} }}"
        elif self.alias is not None and self.additional_info is None:
            return f"{self.alias} = {{ {str(self.state) } }}"
        elif self.alias is None and self.additional_info is None:
            return f"{{ {str(self.state)} }}"


@dataclass
class AutomateRow:
    table_state: TableState
    signals: list[str]
    states: list[State]

    def __getitem__(self, item: str) -> State:
        return self.states[self.signals.index(item)]

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = [""] + self.signals
        table.add_row(
            [str(self.table_state)] + [self.states[_] for _ in self.states]
        )
        return str(table)


class Automate:
    __signals: list[str]
    __states: list[TableState]
    __matrix: list[list[State]] = []

    def __init__(
            self,
            states: list[TableState] | list[TableStateDict] | None = None,
            signals: list[str] | None = None,
            automate_dict: AutomateDict | None = None
    ) -> None:
        self.__matrix = []
        if states is not None and signals is not None:
            self.__signals = signals
            if isinstance(states, list) and len(states) == 0:
                self.__states = states
            elif isinstance(states[0], TableState):
                self.__states = states
            elif isinstance(states[0], dict) or isinstance(states[0], TableStateDict):
                self.__states = [AutomateUtils.create_table_state_from_dict(_) for _ in states]
            self.__fill_clear_matrix()
        elif automate_dict is not None:
            self.__states = [AutomateUtils.create_table_state_from_dict(_) for _ in automate_dict["table_states"]]
            self.__signals = automate_dict["table_signals"]
            self.__fill_clear_matrix()

            for state in self.__states:
                for signal in self.__signals:
                    self.__setitem__(
                        (state.alias, signal),
                        automate_dict["states"][self.__get_state_index_by_alias(state.alias)][self.__get_signal_index_by_name(signal)]
                    )

    @property
    def signals_count(self) -> int:
        return len(self.__signals)

    @property
    def states_count(self) -> int:
        return len(self.__states)

    def get_states_alias(self) -> list[str]:
        return [_.alias for _ in self.__states]

    def get_signals_name(self) -> list[str]:
        return self.__signals

    def get_state_by_id(self, state_id: int) -> TableState:
        return self.__states[state_id]

    def get_signal_by_id(self, signal_id: int) -> str:
        return self.__signals[signal_id]

    def __get_state_index_by_alias(self, item: str) -> int:
        index = 0
        for state in self.__states:
            if state.alias == item:
                return index
            index += 1

    def __get_signal_index_by_name(self, name: str) -> int:
        index = 0
        for signal in self.__signals:
            if signal == name:
                return index
            index += 1

    def __fill_clear_matrix(self):
        for state in self.__states:
            row = []
            for signal in self.__signals:
                row.append(State({""}))
            self.__matrix.append(row)

    def __getitem__(self, item: str | tuple[str, str]) -> AutomateRow | State:
        if isinstance(item, tuple) and len(item) == 2:
            return self.__matrix[self.__get_state_index_by_alias(item[0])][self.__get_signal_index_by_name(item[1])]
        elif isinstance(item, str):
            c_state_alias = self.__get_state_index_by_alias(item)
            return AutomateRow(
                self.__states[c_state_alias],
                self.__signals,
                self.__matrix[self.__get_state_index_by_alias(item)]
            )
        else:
            raise KeyError("Неверный индекс")

    def __setitem__(self, item: tuple[str, str], value: list[str] | State) -> None:
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(value, State):
                self.__matrix[self.__get_state_index_by_alias(item[0])][self.__get_signal_index_by_name(item[1])] = value
            else:
                self.__matrix[self.__get_state_index_by_alias(item[0])][self.__get_signal_index_by_name(item[1])] = State(set(value))

    def __str__(self) -> str:
        return self.to_string()

    def __get_row_elements(
            self,
            alias: str,
            highlighted_states: list[StateDict] | None = None
    ) -> list[str]:
        row = []
        if highlighted_states is not None:
            for i in self.__signals:
                for j in highlighted_states:
                    if alias == j["state_alias"] and i == j["signal_name"]:
                        row.append(f"( {str(self[alias, i])} )")
                    else:
                        row.append(f"{str(self[alias, i])}")
        else:
            for i in self.__signals:
                row.append(f"{str(self[alias, i])}")

        return row


    def to_dict(self) -> AutomateDict:
        s = []

        for row in self.__matrix:
            t = []
            for column in row:
                t.append(list(column.value))
            s.append(t)

        return AutomateDict(
            table_states=self.__get_table_states_to_dict(),
            table_signals=self.__signals,
            states=s
        )

    def __get_table_states_to_dict(self) -> list[TableStateDict]:
        table_states = []
        for i in self.__states:
            table_states.append(TableStateDict(
                state=list(i.state.value),
                alias=i.alias,
                additional_info=i.additional_info,
                is_start=i.is_start,
                is_end=i.is_end
            ))
        return table_states

    def get_all_states(self) -> list[str]:
        states = set(self.get_states_alias())
        for state in self.__states:
            states |= state.state.value
        return sorted(states)

    def get_all_table_states_obj(self) -> list[TableState]:
        return self.__states

    def check_correct_states(self, states_check: list[str]) -> bool:
        states = set(self.get_states_alias())
        for state in self.__states:
            states |= state.state.value
        for state in states_check:
            if state not in states:
                return False
        return True

    def check_is_all_states_in(self, states_check: list[str]) -> bool:
        states = set(self.get_all_states())
        for state_check in states_check:
            if state_check not in states:
                return False
        return True

    def check_is_all_signals_in(self, signals_check: list[str]) -> bool:
        for signal_check in self.__signals:
            if signal_check not in signals_check:
                return False
        return True

    def set_start_state_by_alias(self, aliases: list[str]) -> None:
        for i in aliases:
            for j in self.__states:
                if i == j.alias:
                    j.is_start = True

    def set_end_state_by_alias(self, aliases: list[str]) -> None:
        for i in aliases:
            for j in self.__states:
                if i == j.alias:
                    j.is_end = True

    def add_state_row(self, state: TableState) -> None:
        self.__states.append(state)
        self.__matrix.append([State({""}) for _ in self.__signals])

    def get_table_state_by_alias(self, alias: str) -> TableState:
        i = 0
        for state in self.__states:
            if state.alias == alias:
                return self.__states[i]
            i += 1

    def get_started_table_state_aliases(self) -> list[str]:
        r = []
        for i in self.__states:
            if i.is_start:
                r.append(i.alias)
        return r

    def get_ended_table_state_aliases(self) -> list[str]:
        r = []
        for i in self.__states:
            if i.is_end:
                r.append(i.alias)
        return r

    def get_not_ended_table_state_aliases(self) -> list[str]:
        r = []
        for i in self.__states:
            if not i.is_end:
                r.append(i.alias)
        return r

    def is_table_state_ended_by_alias(self, alias: str) -> bool:
        for state in self.__states:
            if state.alias == alias:
                return state.is_end

    def is_deterministic(self) -> bool:
        for state in self.__states:
            for signal in self.__signals:
                transitions = self[state.alias, signal].value
                if len(transitions) > 1:
                    return False
        return True

    def to_string(self, highlighted_states: list[StateDict] | None = None) -> str:
        table = PrettyTable()
        table.field_names = [""] + self.__signals
        for item in self.__states:
            table.add_row(
                [str(item)] + self.__get_row_elements(item.alias, highlighted_states)
            )
        return str(table)

    def sort_table_states(self) -> None:
        sorted_indices = sorted(range(len(self.__states)), key=lambda i: self.__states[i].alias)

        self.__states = [self.__states[i] for i in sorted_indices]
        self.__matrix = [self.__matrix[i] for i in sorted_indices]

class AutomateUtils:
    @staticmethod
    def create_table_state_from_dict(table_state_dict: TableStateDict) -> TableState:
        return TableState(
            state=State(set(table_state_dict["state"])),
            alias=table_state_dict["alias"],
            additional_info=table_state_dict["additional_info"],
            is_start=table_state_dict["is_start"],
            is_end=table_state_dict["is_end"]
        )
