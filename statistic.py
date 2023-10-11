import json

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from ydata_profiling import ProfileReport


class Statistic:

    def __init__(self, user_nat, user_var, user_date, raw_df):
        self.user_var = user_var
        self.user_date = user_date
        self.raw_df = raw_df
        self.user_nat = user_nat
        self.df = None
        self.df_list = []

    def configure_plots(self, ax):
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.title(f"Graph of {', '.join(self.user_var)} for {self.user_nat}")
        plt.legend()

    def clean_data(self):
        date_filtered_df = self.raw_df.loc[
            (self.raw_df.index >= self.user_date) & (self.raw_df.index <= self.raw_df.index.max())]
        df_cleared = date_filtered_df.dropna(how="all")
        for nat in self.user_nat:
            nat_filtered_df = pd.DataFrame(df_cleared[df_cleared['location'].str.contains(nat)])
            filtered_df = nat_filtered_df[self.user_var]
            if not filtered_df.empty:
                self.df_list.append(filtered_df)

    def generate_individual_plots(self):
        for df, nat in zip(self.df_list, self.user_nat):
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index, df, label=f"{nat}, {self.user_var}")
            self.configure_plots(ax)
            plt.show()
        self.generate_reports()

    def generate_combined_plot(self):
        if not self.df_list:
            print("Brak danych do wygenerowania wykresu.")
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        for df, nat in zip(self.df_list, self.user_nat):
            for var in self.user_var:
                ax.plot(df.index, df[var], label=f"{nat}, {var}")
        self.configure_plots(ax)
        plt.show()
        self.generate_reports()

    def generate_reports(self):
        for df, nat in zip(self.df_list, self.user_nat):
            print(f"Opis statstyczny dla {nat}")
            print(df.describe())
            user_input = input("Czy chcesz wygenerować pelny raport? (Tak/Nie): ").strip().lower()
            if user_input.lower() == "tak":
                profile = ProfileReport(df, title="report")
                profile.to_file("report.json")

    def read_reports(self):
        with open("report.json", "r") as json_file:
            report = json.load(json_file)
        sections_to_display = ["analysis", "table", "variables", "correlations"]
        keys_to_exclude = ["value_counts_without_nan", "value_counts_index_sorted", "histogram"]
        for section_name in sections_to_display:
            if section_name in report:
                section_data = report[section_name]
                print(section_name)
                if section_name == "variables":
                    for var_name in self.user_var:
                        if var_name in section_data:
                            var_data = section_data[var_name]
                            print(f"Variable: {var_name}")
                            if isinstance(var_data, dict):
                                for i, (key, value) in enumerate(var_data.items(), start=1):
                                    if key not in keys_to_exclude:
                                        print(f"{i}. {key}: {value}")
                            else:
                                print(f"Zmienna {var_name} nie jest slownikiem w raporcie")
                        else:
                            print(f"Zmienna {var_name} nie istnieje w raporcie")
                elif section_name == "correlations":
                    if isinstance(section_data, dict):
                        for correlation_key, correlation_list in section_data.items():
                            if isinstance(correlation_list, list):
                                for correlation_data in correlation_list:
                                    if isinstance(correlation_data, dict):
                                        for i, (key, value) in enumerate(correlation_data.items(), start=1):
                                            if key not in keys_to_exclude:
                                                if len(self.user_var) <= 2:
                                                    if i == 1:
                                                        print(f"{i}. {key}: {value}")
                                                else:
                                                    print(f"{i}. {key}: {value}")
                                    else:
                                        print(f"Nieobslugiwany typ danych w sekcji {section_name}")
                            else:
                                print(f"Sekcja {section_name} nie jest lista w raporcie")
                    else:
                        print(f"Sekcja {section_name} nie jest slownikiem w raporcie")
                else:
                    if isinstance(section_data, dict):
                        for i, (key, value) in enumerate(section_data.items(), start=1):
                            if key not in keys_to_exclude:
                                print(f"{i}. {key}: {value}")
                    else:
                        print(f"Nieobsługiwany typ danych w sekcji {section_name}")
            else:
                print(f"Sekcja {section_name} nie istnieje w raporcie")
