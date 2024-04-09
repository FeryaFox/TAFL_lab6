class BaseInputer:

    def _input_alphabet(self, input_phrase,) -> list[str] | None:
        while True:
            try:
                alphabet = input(input_phrase).split()
            except KeyboardInterrupt:
                return None

            if not alphabet:
                return None

            if self._check_correct_alphabet(alphabet):
                continue
            break

        return alphabet

    def _check_correct_alphabet(self, alphabet: list[str]) -> bool:
        j = 0
        error = False
        for i in alphabet:
            if i in alphabet[j + 1:]:
                print("Вы ввели недопустимый алфавит. В веденном алфавите есть повторяющийся символ.")
                error = True
                break

            # if len(i) != 1:
            #     error = True
            #     print("Вы ввели недопустимый алфавит. Скорее всего вы ввели двойной символ")
            #     break

            j += 1
            if error:
                break
        return error
