class Variables:
    def __init__(self, raw_df):
        self.raw_df = raw_df
        self.nationality_list = list(raw_df["location"].unique())
        self.list_of_variables = list(raw_df.columns)
        self.args = []
        self.a = 0

    def nationality(self):
        user_nat = input("Podaj z jakiej narodowosci maja zostac podane dane: ").capitalize()
        if user_nat in self.nationality_list:
            return user_nat

    def selecting_variables(self):
        user_input = int(input("Podaj ile danych chcesz porownac: "))
        while self.a < user_input:
            user_variable = input("Podaj zmienna do analizy: ")
            if user_variable in self.list_of_variables:
                self.args.append(user_variable)
                self.a += 1
            else:
                print("Podana zmienna nie jest obslugiwana")
        return self.args
