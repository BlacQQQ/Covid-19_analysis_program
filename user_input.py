def int_input(prompt):
    while True:
        try:
            user_inp = int(input(prompt))
            return user_inp
        except ValueError:
            print("Proszę podać cyfrę z zakresu")


def str_input(prompt):
    while True:
        try:
            user_inp = input(prompt)
            if user_inp.strip():
                return user_inp.strip().lower()
            else:
                raise ValueError("Nie wprowadzono żadnych danych.")
        except ValueError:
            print("Prosze podac tak lub nie")
