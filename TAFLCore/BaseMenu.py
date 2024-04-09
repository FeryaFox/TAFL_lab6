import os


def check_is_correct_linux_terminal_environment() -> bool:
    if os.name != "posix" or "PYCHARM_HOSTED" in os.environ or "TERM" not in os.environ or os.environ["TERM"] == "":
        return False

    try:
        import simple_term_menu
    except ModuleNotFoundError:
        return False

    return True


correct_linux_terminal = check_is_correct_linux_terminal_environment()

if correct_linux_terminal:
    from simple_term_menu import TerminalMenu


class BaseMenu:
    __correct_linux_terminal: bool = None

    def __init__(self):
        self.__correct_linux_terminal = self.check_is_correct_linux_terminal_environment()

    @staticmethod
    def check_is_correct_linux_terminal_environment() -> bool:
        return check_is_correct_linux_terminal_environment()

    @staticmethod
    def is_posix() -> bool:
        if os.name == "posix":
            return True
        return False

    @property
    def correct_linux_terminal(self):
        if self.__correct_linux_terminal is None:
            self.__correct_linux_terminal = self.check_is_correct_linux_terminal_environment()
        return self.__correct_linux_terminal

    def get_choose(self, choose: list, ignore_keyboard_interrupt: bool = False) -> int | None:

        if self.correct_linux_terminal:
            while True:
                menu = TerminalMenu(choose)
                menu.show()
                if menu.chosen_menu_index is None and ignore_keyboard_interrupt:
                    continue
                return menu.chosen_menu_index
        else:
            while True:
                for i in range(0, len(choose)):
                    print(f"{i+1}) - {choose[i]}")
                try:
                    choose_ = int(input("Выберите пункт меню: "))
                    if choose_ < 1 or choose_ > len(choose):
                        continue
                    return choose_ - 1
                except ValueError:
                    continue
                except KeyboardInterrupt:
                    if ignore_keyboard_interrupt:
                        continue
                    return None

    @staticmethod
    def clear_wrapper(func):
        def wrapper(self, *args, **kwargs):
            self.clear()
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def clear() -> None:
        if not ("TERM" not in os.environ or os.environ["TERM"] == "") and os.name == "posix":
            # Когда запущено в линуксаих в нормальном терминале
            ...
            os.system('cls' if os.name == 'nt' else 'clear')
        elif os.name == "posix" or "PYCHARM_HOSTED" in os.environ:
            # когда запущено в pycharm
            ...
        elif os.name == "nt":
            # когда запущено в винде в командной строке
            os.system('cls')
