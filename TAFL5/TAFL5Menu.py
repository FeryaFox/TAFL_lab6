from TAFLCore.BaseMenu import BaseMenu


class TAFL5Menu(BaseMenu):

    @BaseMenu.clear_wrapper
    def use_save_config_menu(
            self,
            previous_alphabet_symbol: list[str],
            previous_alphabet_graph: list[str],
            previous_automate: str
    ) -> int:
        print("Уже есть загруженные данные. Хотите использовать его?")
        print(f"Уже есть сохраненный алфавит входных символов '{' '.join(previous_alphabet_symbol)}'.")
        print(f"Уже есть сохраненный алфавит графа '{' '.join(previous_alphabet_graph)}.")
        print(f"Начальный автомат: \n" + previous_automate )
        menu_choice = self.get_choose(
            [
                "Да",
                "Нет"
            ]
        )
        return menu_choice

    @BaseMenu.clear_wrapper
    def change_save_config_menu(self) -> int | None:
        print("Изменить: ")
        menu_choice = self.get_choose(
            [
                "Алфавит входных символов и графа",
                "Начальный автомат",
                "Не хочу ничего менять"
            ]
        )

        return menu_choice

    @BaseMenu.clear_wrapper
    def change_init_configs_menu(self) -> int | None:
        print("Изменить: ")
        menu_choice = self.get_choose(
            [
                "Алфавит входных символов",
                "Алфавит графа",
                "Начальный автомат"
                "Назад"
            ]
        )

        return menu_choice

    @BaseMenu.clear_wrapper
    def main_menu(self) -> int:
        menu_choice = self.get_choose(
            [
                "Показать данные",
                "Основное задание",
                "Проверить слово",
                "Изменить входные данные",
                "Выход"
            ]
        )
        return menu_choice
