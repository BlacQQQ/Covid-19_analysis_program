import pandas as pd

import data_frame
import files
import statistic
import user_input


class Main:
    def __init__(self):
        self.raw_df = pd.read_csv("covid_data.csv", index_col="date")
        self.raw_df.index = pd.to_datetime(self.raw_df.index, format="%Y-%m-%d")
        self.var = data_frame.Variables(self.raw_df)
        self.user_input = user_input
        self.user_nat = None
        self.user_var = None
        self.user_date = None

    @staticmethod
    def display_menu():
        print("1. Rozpocznij analizę statystyczną")
        print("2. Wczytaj parametry z pliku")
        print("3. Wyjście")

    @staticmethod
    def display_sub_menu():
        print("1. Statystyka opisowa")
        print("2. Wykresy")
        print("3. Statystyka matematyczna")
        print("4. Zapisz wybrane dane do pliku konfiguracyjnego")
        print("5. Powrót")

    def main_menu(self):
        # files.download_or_update_covid_data()
        self.display_menu()
        program_menu = self.user_input.int_input("Wybierz, co chcesz zrobić: ")
        match program_menu:
            case 3:
                return False
            case 2:
                config_data = files.Config.load_config_from_file()
                if config_data is not None:
                    self.user_nat, self.user_var, self.user_date = files.Config.extract_config(config_data)
                    if self.user_nat is not None:
                        self.sub_menu()
                    else:
                        return True
            case 1:
                self.user_nat = self.var.nationality()
                if self.user_nat is None:
                    return True
                self.user_var = self.var.variables()
                if self.user_var is None:
                    return True
                self.user_date = self.var.date_index()
                if self.user_date is None:
                    return True
                self.sub_menu()
        return True

    def sub_menu(self):
        self.display_sub_menu()
        stat = statistic.Statistic(self.user_nat, self.user_var, self.user_date, self.raw_df)
        stat.clean_data()
        menu_for_1_nat = self.user_input.int_input("Wybierz, co chcesz zrobić: ")
        match menu_for_1_nat:
            case 5:
                del self.user_var, self.user_date, self.user_nat
            case 1:
                descriptive_statistics_menu = self.user_input.int_input(
                    "1. Wykonać statystyke opisową dla podanych danych\n"
                    "2. Wczytać istniejący plik z reportem\n"
                    "Wybierz, co chcesz zrobić: ")
                if descriptive_statistics_menu == 1:
                    stat.generate_reports()
                    user_choice = self.user_input.int_input(
                        "1. Czy chcesz wczytać powstały raport? (Tak/Nie): ")
                    if user_choice == "tak":
                        stat.read_reports()
                    elif user_choice == "nie":
                        pass
                elif descriptive_statistics_menu == 2:
                    stat.read_reports()
            case 2:
                graph_menu = self.user_input.int_input(
                    "1. Wspólny wykres\n"
                    "2. 2 osobne wykresy\n"
                    "Wybierz, co chcesz zrobić: ")
                if graph_menu == 1:
                    stat.generate_combined_plot()
                elif graph_menu == 2:
                    stat.generate_individual_plots()
                    user_choice = self.user_input.str_input("Czy chcesz wygenerować raport? (Tak/Nie): ")
                    if user_choice == "tak":
                        stat.generate_reports()
                    elif user_choice == "nie":
                        pass
            case 3:
                print("work in progress")
            case 4:
                file = files.Config(self.user_nat, self.user_var, self.user_date)
                file.save_config_to_file()


if __name__ == "__main__":
    main = Main()
    while main.main_menu():
        pass
