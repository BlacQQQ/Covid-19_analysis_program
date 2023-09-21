from datetime import datetime, date
from enum import IntEnum

import pandas as pd
from dateutil.relativedelta import relativedelta

import statistic
import variables


class ProgramMenu(IntEnum):
    statistic_for_1_country = 1
    statistic_for_more_country = 2
    exit = 3


class DataMenu(IntEnum):
    last_2_weeks = 1
    last_month = 2
    last_3_months = 3
    last_half_year = 4
    last_year = 5
    all_time = 6
    custom_time = 7


def selecting_nationalities_for_statistics(raw_df):
    nationality_list = list(raw_df["location"].unique())
    user_input = input("Podaj w jezyku angielskim z jakiej narodowosci maja zostac podane dane: ").capitalize()
    if user_input in nationality_list:
        return user_input
    else:
        print("Podana nazwa panstwa nie zostala znaleziona w bazie danych, sprobuj wpisac ponownie")
        selecting_nationalities_for_statistics(raw_df)


def date_range(DataMenu, start_date, end_date):
    print("1. z 2 ostatnich tygodni")
    print("2. z ostatniego miesiaca")
    print("3. z ostatnich 3 miesiecy")
    print("4. z ostatniego pol roku")
    print("5. z ostatniego roku")
    print("6. caly okres dostepy w bazie")
    print("7. zakres customowy")
    user_input = int(input("Podaj z jakiego okresu czasu maja zostac przeanalizowane dane: "))
    match user_input:
        case DataMenu.last_2_weeks:
            return datetime.now() - relativedelta(days=14)
        case DataMenu.last_month:
            return datetime.now() - relativedelta(months=1)
        case DataMenu.last_3_months:
            return datetime.now() - relativedelta(months=3)
        case DataMenu.last_half_year:
            return datetime.now() - relativedelta(months=6)
        case DataMenu.last_year:
            return datetime.now() - relativedelta(years=1)
        case DataMenu.all_time:
            return None
        case DataMenu.custom_time:
            while True:
                date_components = input("Podaj date w formacie YYYY-MM-DD: ").split("-")
                year, month, day = [int(item) for item in date_components]
                user_date = date(year, month, day)
                if user_date < start_date or user_date > end_date:
                    print(
                        f"Podany zakres daty nie miesci sie w zakresie bazy danych, minimalny zakres to {start_date}, maksymalny to {end_date}")
                else:
                    return user_date


raw_df = pd.read_csv("covid_data.csv", index_col="date")
# downloading_file.downloading_file_from_github()
while True:
    print("1. Ropocznij analize statystyczna dla 1 panstwa")
    print("2. Rozpocznij analize statystyczna dla 2 panstw (work in progress)")
    print("3. Wyjscie")
    menu = int(input("Wybierz, co chcesz zrobic: "))
    match menu:
        case ProgramMenu.exit:
            exit()
        case ProgramMenu.statistic_for_1_country:
            chosen_nat = selecting_nationalities_for_statistics(raw_df)
            args = variables.selecting_variables(raw_df)
            start_date = pd.to_datetime(raw_df.index.min()).date()
            end_date = pd.to_datetime(raw_df.index.max()).date()
            index_date = date_range(DataMenu, start_date, end_date)
            if index_date is None:
                print(index_date)
                index_date = start_date
            statistic.statistical_analysis(chosen_nat, args, raw_df, index_date)
        case ProgramMenu.statistic_for_more_country:
            print("work in progress")