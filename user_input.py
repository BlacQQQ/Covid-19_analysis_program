def int_input(prompt):
    while True:
        try:
            user_inp = int(input(prompt))
            return user_inp
        except ValueError:
            print("Please enter a digit")


def str_input(prompt):
    while True:
        try:
            user_inp = input(prompt)
            if user_inp.strip():
                return user_inp.strip().lower()
            else:
                raise ValueError("No data has been entered")
        except ValueError:
            print("Please indicate yes or no")
