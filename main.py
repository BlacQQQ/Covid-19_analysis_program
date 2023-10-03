import pandas as pd

import downloading_file
import index_df
import statistic
import variables

downloading_file.downloading_file_from_github()
raw_df = pd.read_csv("covid_data.csv", index_col="date")
raw_df.index = pd.to_datetime(raw_df.index, format="%Y-%m-%d")
datamenu = index_df.DataMenu(raw_df)
while True:
    print("1. Ropocznij analize statystyczna dla 1 panstwa")
    print("2. Rozpocznij analize statystyczna dla 2 panstw (work in progress)")
    print("3. Wyjscie")
    program_menu = int(input("Wybierz, co chcesz zrobic: "))
    var = variables.Variables(raw_df)
    if program_menu == 3:
        exit()
    elif program_menu == 1 or program_menu == 2:
        user_nat = []
        digits_of_nat = 1
        if program_menu == 2:
            digits_of_nat = int(input("Ile krajow chcesz porownac?"))
        for _ in range(digits_of_nat):
            user_nat.append(var.nationality())
        user_var = var.selecting_variables()
        user_date = datamenu.index_range()
        stat = statistic.Statistic(user_nat, user_var, user_date, raw_df)
        arg_for_statistic = stat.process_data()
        print("1. Statystyka opisowa")
        print("2. Statystyka matematyczna")
        print("3. Wykresy")
        print("4. Powrot")
        menu_for_1_nat = int(input("Wybierz, co chcesz zrobic:"))
        match menu_for_1_nat:
            case 4:
                pass
            case 1:
                arg_for_statistic.long_report()
            case 2:
                print("work in progress")
            case 3:
                arg_for_statistic.graphs()
