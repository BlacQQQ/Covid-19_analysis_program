from datetime import datetime

from dateutil.relativedelta import relativedelta

import user_input


class Variables:
    def __init__(self, raw_df):
        self.user_input = user_input
        self.raw_df = raw_df
        self.start_date = self.raw_df.index.min()
        self.end_date = self.raw_df.index.max()
        self.list_of_variables = list(raw_df.columns)
        self.list_of_continents = raw_df.continent.unique()

    def nationality(self):
        cleaned_list_of_con = sorted([x for x in self.list_of_continents if x == x])
        list_of_user_nat = []
        while True:
            for count, con in enumerate(sorted(cleaned_list_of_con), start=1):
                print(count, con)
            print("To go back enter 0")
            user_con = self.user_input.int_input("Enter the continent to analyze: ")
            if user_con == 0:
                break
            elif user_con < 0:
                print("Please enter a number in the range given above")
                continue
            user_con -= 1
            try:
                list_of_nat = sorted(
                    self.raw_df.query(f"continent == '{cleaned_list_of_con[user_con]}'")["location"].unique())
            except IndexError:
                print("Please enter a number in the range given above")
                continue
            for count, nat in enumerate(list_of_nat, start=1):
                print(count, nat)
            print("To go back, enter 0 \n"
                  "To stop adding countries type -1")
            while True:
                user_nat = self.user_input.int_input("Enter the country for analysis: ")
                if user_nat == -1 and len(list_of_user_nat) > 0:
                    return list_of_user_nat
                elif user_nat == 0:
                    break
                elif 1 <= user_nat <= len(list_of_nat):
                    user_nat -= 1
                    list_of_user_nat.append(list_of_nat[user_nat])
                else:
                    print("Please enter a number in the range given above")
                continue

    def variables(self):
        del self.list_of_variables[:3], self.list_of_variables[13]
        list_of_user_var = []
        while True:
            print("1. Confirmed cases and deaths \n"
                  "2. Hospital & ICU \n"
                  "3. Tests & positivity \n"
                  "4. Vaccinations \n"
                  "5. Excess mortality \n"
                  "6. Others \n")
            user_group_var = user_input.int_input("Which group of variables interests you: ")
            try:
                if 1 <= user_group_var <= 6:
                    group_variables = []
                    if user_group_var == 1:
                        group_variables = sorted(self.list_of_variables[0:12])
                    elif user_group_var == 2:
                        group_variables = sorted(self.list_of_variables[12:20])
                    elif user_group_var == 3:
                        group_variables = sorted(self.list_of_variables[20:29])
                    elif user_group_var == 4:
                        group_variables = sorted(self.list_of_variables[29:42])
                    elif user_group_var == 5:
                        group_variables = sorted(self.list_of_variables[57:62])
                    elif user_group_var == 6:
                        group_variables = sorted(self.list_of_variables[42:57])
                    for count, var in enumerate(group_variables, start=1):
                        print(count, var)
                    print("To go back, enter 0 \n"
                          "To stop adding countries type -1")
                    while True:
                        user_var = user_input.int_input("Which variable you are interested in: ")
                        if user_var == 0:
                            return False
                        elif user_var == -1 and len(list_of_user_var) > 0:
                            return list_of_user_var
                        elif 1 <= user_var <= len(group_variables):
                            user_var -= 1
                            list_of_user_var.append(group_variables[user_var])
                        else:
                            print("Please enter a number in the range given above")
                            continue
            except ValueError:
                print("Invalid input, please enter a number between 1 and 6")
                continue
            except IndexError:
                print("The value provided is outside the range of the list")
                continue


class TimePeriod:

    @staticmethod
    def custom_date(var):
        while True:
            date_str = user_input.str_input("Enter the date in YYYY-MM-DD format: ")
            try:
                user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if var.start_date <= user_date <= var.end_date:
                    return user_date
                else:
                    print(f"The specified date is outside the valid range: {var.start_date} - {var.end_date}")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

    @staticmethod
    def date_index(var: Variables):
        print("1. From the last 2 weeks\n"
              "2. Last month\n"
              "3. From the last 3 months\n"
              "4. Over the past six months\n"
              "5. Last year\n"
              "6. All-time period in the database\n"
              "7. Custom range")
        while True:
            user_time = user_input.int_input("Specify the time period for data analysis: ")
            if user_time is not None:
                if user_time == 1:
                    return datetime.now() - relativedelta(days=14)
                elif user_time == 2:
                    return datetime.now() - relativedelta(months=1)
                elif user_time == 3:
                    return datetime.now() - relativedelta(months=3)
                elif user_time == 4:
                    return datetime.now() - relativedelta(months=6)
                elif user_time == 5:
                    return datetime.now() - relativedelta(years=1)
                elif user_time == 6:
                    return var.start_date
                elif user_time == 7:
                    return TimePeriod.custom_date(var)
                else:
                    print("Please select a number from range abow")
            else:
                print("Please select a valid option")
