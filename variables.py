from pprint import pprint

import pandas as pd


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
