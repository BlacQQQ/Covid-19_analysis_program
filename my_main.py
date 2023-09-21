from enum import IntEnum
from pprint import pprint

import pandas as pd

import downloading_file


class ProgramMenu(IntEnum):
    wybranie_zmiennych = 1
    lista_zmiennych = 2
    powrot = 3


def selecting_nationalities_for_statistics(df):
    nationality_list = list(df["location"].unique())
    user_input = input("Podaj w jezyku angielskim z jakiej narodowosci maja zostac podane dane: ").capitalize()
    if user_input in nationality_list:
        return user_input
    else:
        print("Podana nazwa panstwa nie zostala znaleziona w bazie danych, sprobuj wpisac ponownie")
        selecting_nationalities_for_statistics(df)


def menu_of_analysing_data(raw_df):
    while True:
        menu = int(input(""""Wybierz, co chcesz zrobic:
        1. Wybrac zmienne do analizy
        2. Wyswietlic liste dostepnych zmiennych wraz z opisem
        3. Powrot
        """))
        if menu == ProgramMenu.powrot:
            exit()
        elif menu == ProgramMenu.wybranie_zmiennych:
            return selecting_variables(raw_df)
        elif menu == ProgramMenu.lista_zmiennych:
            dict_of_variables()


def dict_of_variables():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-codebook.csv"
    df = pd.read_csv(url)
    df_dict = df[["column", "description"]].set_index("column").T.to_dict("list")
    pprint(df_dict)


def selecting_variables(raw_df):
    list_of_variables = list(raw_df.columns)
    args = []
    a = 0
    try:
        user_input = int(input("Podaj ile danych chcesz porownac: "))
        while a < user_input:
            user_variable = input("Podaj zmienna do analizy: ")
            if user_variable in list_of_variables:
                args.append(user_variable)
                a += 1
            else:
                print("Podana zmienna nie jest obslugiwana")
        return args
    except ValueError:
        print("Nie podales cyfry")
        selecting_variables(raw_df)


def statistical_analysis(chosen_nat, args, raw_df):
    df = raw_df[[args]]
    print(df)
    df = df[df["location"].str.contains(chosen_nat)]
    print(df)


# def graphs(df_pol, args):
#     df_pol[args].plot()
#     user_input = input("Chcesz zapisac wykres? Tak lub nie: ")
#     if user_input.capitalize() == "Tak":
#         plt.savefig("fig.jpg", format="jpg")
#     plt.show()
#
#
downloading_file.downloading_file_from_github()
raw_df = pd.read_csv("covid_data.csv", index_col="date")
print(raw_df)
chosen_nat = selecting_nationalities_for_statistics(raw_df)
args = menu_of_analysing_data(raw_df)
statistical_analysis(chosen_nat, args, raw_df)
# print(df_nat[args].to_string())
# graphs(df_nat, args)
