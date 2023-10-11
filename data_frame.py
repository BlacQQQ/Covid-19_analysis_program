from datetime import datetime, date

from dateutil.relativedelta import relativedelta

import user_input


class Variables:
    last_2_weeks = 1
    last_month = 2
    last_3_months = 3
    last_half_year = 4
    last_year = 5
    all_time = 6
    custom_time = 7

    def __init__(self, raw_df):
        self.user_input = user_input
        self.start_date = raw_df.index.min()
        self.end_date = raw_df.index.max()
        self.raw_df = raw_df
        self.list_of_variables = list(raw_df.columns)
        self.list_of_continents = raw_df.continent.unique()
        self.args = []
        self.nat = []

    def nationality(self):
        cleaned_list_of_con = sorted([x for x in self.list_of_continents if x == x])
        while True:
            for count, con in enumerate(sorted(cleaned_list_of_con), start=1):
                print(count, con)
            print("Aby wrocic podaj 0")
            try:
                user_con = self.user_input.int_input("Podaj kontynent do analizy: ")
                if user_con == 0:
                    return
                user_con -= 1
                list_of_nat = sorted(
                    self.raw_df.query(f"continent == '{cleaned_list_of_con[user_con]}'")["location"].unique())
            except IndexError:
                print("Prosze podac cyfre, w zakresie podanym wyzej")
                continue
            for count, nat in enumerate(list_of_nat, start=1):
                print(count, nat)
            print("Aby sie cofnac wpisz 0")
            print("Aby zakonczyc dodawanie panstw wpisz -1")
            while True:
                user_nat = self.user_input.int_input("Podaj panstwo do analizy: ")
                if user_nat == -1 and len(self.nat) > 0:
                    return self.nat
                elif user_nat == 0:
                    break
                elif 1 <= user_nat <= len(list_of_nat):
                    user_nat -= 1
                    self.nat.append(list_of_nat[user_nat])
                else:
                    print("Prosze podac cyfre, w zakresie podanym wyzej")
                continue

    def variables(self):
        del self.list_of_variables[:3]
        del self.list_of_variables[13]
        while True:
            print("1. Confirmed cases and deaths \n"
                  "2. Hospital & ICU \n"
                  "3. Tests & positivity \n"
                  "4. Vaccinations \n"
                  "5. Excess mortality \n"
                  "6. Others \n")
            user_group_var = user_input.int_input("Ktora grupa zmiennych cie interesuje: ")
            match user_group_var:
                case 1:
                    for count, var in enumerate(sorted(self.list_of_variables[0:12]), start=1):
                        print(count, var)
                case 2:
                    for count, var in enumerate(sorted(self.list_of_variables[12:20]), start=1):
                        print(count, var)
                case 3:
                    for count, var in enumerate(sorted(self.list_of_variables[20:29]), start=1):
                        print(count, var)
                case 4:
                    for count, var in enumerate(sorted(self.list_of_variables[29:42]), start=1):
                        print(count, var)
                case 5:
                    for count, var in enumerate(sorted(self.list_of_variables[57:62]), start=1):
                        print(count, var)
                case 6:
                    for count, var in enumerate(sorted(self.list_of_variables[42:57]), start=1):
                        print(count, var)
            print("Aby cie cofnac podaj 0")
            while True:
                user_var = user_input.int_input("Ktora zmienna cie interesuje: ")
                if user_var == 0:
                    break
                elif user_var == -1 and len(self.args) > 0:
                    return self.args
                elif user_var == 0:
                    return
                elif user_var in self.list_of_variables:
                    return self.args
                elif 1 <= user_var <= len(self.list_of_variables):
                    user_var -= 1
                    self.args.append(self.list_of_variables[user_var])
                else:
                    print("Prosze podac cyfre, w zakresie podanym wyzej")
                    continue

    def date_index(self):
        print("1. z 2 ostatnich tygodni")
        print("2. z ostatniego miesiaca")
        print("3. z ostatnich 3 miesiecy")
        print("4. z ostatniego pol roku")
        print("5. z ostatniego roku")
        print("6. caly okres dostepy w bazie")
        print("7. zakres customowy")
        user_time = user_input.int_input("Podaj z jakiego okresu czasu maja zostac przeanalizowane dane: ")
        match user_time:
            case self.last_2_weeks:
                return datetime.now() - relativedelta(days=14)
            case self.last_month:
                return datetime.now() - relativedelta(months=1)
            case self.last_3_months:
                return datetime.now() - relativedelta(months=3)
            case self.last_half_year:
                return datetime.now() - relativedelta(months=6)
            case self.last_year:
                return datetime.now() - relativedelta(years=1)
            case self.all_time:
                user_date = self.start_date
                return user_date
            case self.custom_time:
                return self.get_custom_date()

    def get_custom_date(self):
        while True:
            date_components = user_input.str_input("Podaj date w formacie YYYY-MM-DD: ").split("-")
            year, month, day = [int(item) for item in date_components]
            user_date = date(year, month, day)
            if user_date < self.start_date or user_date > self.end_date:
                print(
                    f"Podany zakres jest niezgodny, minimalny zakres to {self.start_date}, maksymalny to {self.end_date}")
                continue
            else:
                return user_date
