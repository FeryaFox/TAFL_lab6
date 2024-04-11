import copy

from TAFL5.TAFL5Saver import TAFL5Saver
from TAFL6.TAFL6 import TAFL6
from TAFL5.TAFL5 import TAFL5
from TAFL6.TAFL6Inputer import TAFL6Inputer
from TAFL5.TAFL5Menu import TAFL5Menu
from TAFLCore.Automate import Automate, AutomateUtils, TableState, State


def main():
    tafl = TAFL6()
    tafl5 = TAFL5()
    saver = TAFL5Saver()
    menu = TAFL5Menu()
    inputer = TAFL6Inputer()

    data_load = saver.load_data()

    alphabet_symbol = []
    alphabet_graph = []
    input_automate = None
    automaton_transition = None
    deparmenize_automate = None

    if data_load == {}:
        alphabet_symbol = inputer.get_alphabet_symbol()
        alphabet_graph = inputer.get_alphabet_graph()
        states = []
        for i in alphabet_graph:
            states.append(
                {
                    "state": [i],
                    "alias": i,
                    "additional_info": None,
                    "is_start": False,
                    "is_end": False
                }
            )
        input_automate = Automate(states=states, signals=alphabet_symbol)

        input_automate = inputer.get_input_automate(input_automate)
        input_automate = inputer.get_started_states(input_automate)

        input_automate = inputer.get_ended_states(input_automate)

        saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())
        print(input_automate)
        input()
    else:
        alphabet_symbol = saver.load_alphabet_symbol()
        alphabet_graph = saver.load_alphabet_graph()
        input_automate = Automate(automate_dict=saver.load_input_automate())

        c = menu.use_save_config_menu(
            alphabet_symbol,
            alphabet_graph,
            str(input_automate)
        )
        match c:
            case 0:
                ...
            case 1:
                alphabet_symbol_ = inputer.get_alphabet_symbol()
                if alphabet_symbol_ is None:
                    ...
                else:
                    alphabet_symbol = alphabet_symbol_
                alphabet_graph_ = inputer.get_alphabet_graph()
                if alphabet_graph_ is None:
                    ...
                else:
                    alphabet_graph = alphabet_graph_
                states = []
                for i in alphabet_graph:
                    states.append(
                        {
                            "state": [i],
                            "alias": i,
                            "additional_info": None,
                            "is_start": False,
                            "is_end": False
                        }
                    )

                input_automate = inputer.get_input_automate(
                    Automate(
                        states=states,
                        signals=alphabet_symbol
                    ),
                    is_change_alphabet=True
                )

                input_automate = inputer.get_started_states(input_automate)
                input_automate = inputer.get_ended_states(input_automate)
                saver.save_all(alphabet_symbol, alphabet_graph, input_automate.to_dict())
                print(input_automate)
                input()

    without_unattainable_stated_automate = tafl.delete_unattainable_stated(input_automate)
    print("Автомат, в котором удалены недостижимые вершины")
    print(without_unattainable_stated_automate)
    if without_unattainable_stated_automate.is_deterministic():
        print("Автомат детерменизированный")
    else:
        print("Автомат недерменизированный")
        without_unattainable_stated_automate = tafl5.deparmenize_automate(without_unattainable_stated_automate)

        print(without_unattainable_stated_automate)
    # Example uцsage:

    print(tafl.partition_equivalence_classes__(without_unattainable_stated_automate))

if __name__ == "__main__":
    main()
