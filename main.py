import os

import pandas as pd

import analysis
import data_frame
import files
import user_input


class Main:
    def __init__(self):
        self.raw_df = pd.read_csv("covid_data.csv", index_col="date")
        self.raw_df.index = pd.to_datetime(self.raw_df.index, format="%Y-%m-%d")
        self.var = data_frame.Variables(self.raw_df)
        self.user_input = user_input
        self.list_of_continents = sorted(self.raw_df["location"].unique())
        self.user_nat = None
        self.user_var = None
        self.user_date = None
        self.update_done = False
        self.list_of_report_names = None

    def main_menu(self):
        if not self.update_done:
            files.download_or_update_covid_data()
            self.update_done = True
        print("1. Start statistical analysis \n"
              "2. Load parameters from a file \n"
              "3. Exit")
        program_menu = self.user_input.int_input("Choose what you want to do: ")
        match program_menu:
            case 3:
                return False
            case 1:
                self.user_nat = self.var.nationality()
                if not self.user_nat:
                    return True
                self.user_var = self.var.variables()
                if not self.user_nat:
                    return True
                self.user_date = data_frame.TimePeriod.date_index(self.var)
                if not self.user_date:
                    return True
                self.sub_menu()
            case 2:
                config = files.Config(self.user_nat, self.user_var, self.user_date).load_from_file()
                if config:
                    self.user_nat, self.user_var, self.user_date = config
                else:
                    return True
                self.sub_menu()
        return True

    def sub_menu(self):
        while True:
            print("1. Descriptive statistics \n"
                  "2. Graphs \n"
                  "3. Mathematical statistics \n"
                  "4. Save the selected data to the configuration file \n"
                  "5. Return")
            data = analysis.Data(self.user_nat, self.user_var, self.user_date, self.raw_df)
            reports = analysis.Reports(self.user_nat, self.user_var, data)
            sub_menu = self.user_input.int_input("Choose what you want to do: ")
            if not sub_menu == 5:
                data.filtered()
            match sub_menu:
                case 5:
                    return False
                case 1:
                    descriptive_statistics_menu = self.user_input.int_input(
                        "1. Perform descriptive statistics for the given data \n"
                        "2. Load an existing report file \n"
                        "Choose what you want to do: ")
                    if descriptive_statistics_menu == 1:
                        self.list_of_report_names = reports.generate()
                    elif descriptive_statistics_menu == 2:
                        if not self.list_of_report_names or len(self.list_of_report_names) < 1:
                            existing_reports = [file for file in os.listdir() if
                                                file.endswith(".json") and file.startswith("Report_for_")]
                            if existing_reports:
                                print("Existing reports: ")
                                for i, existing_report in enumerate(existing_reports, start=1):
                                    print(f"{i}. {existing_report}")
                                selected_report_index = self.user_input.int_input("Select the report to load: ")
                                if 1 <= selected_report_index <= len(existing_reports):
                                    selected_report_name = existing_reports[selected_report_index - 1]
                                    reports.read(selected_report_name)
                                else:
                                    print("Invalid selection")
                            else:
                                print("No existing reports found")
                case 2:
                    available_plot_types = ["Line Plot", "Bar Plot", "Horizontal Bar Plot", "Grouped Bar Plot"]
                    print("Available graph types:")
                    for i, plot_type in enumerate(available_plot_types, start=1):
                        print(f"{i}. {plot_type}")
                    chosen_plot_index = user_input.int_input("Select graph type: ") - 1
                    if chosen_plot_index < 0 or chosen_plot_index >= len(available_plot_types):
                        print("Incorrect selection")
                    else:
                        chosen_plot_type = available_plot_types[chosen_plot_index]
                        graph_menu = self.user_input.int_input(
                            "1. Separate graphs \n"
                            "2. Joint graph \n"
                            "Choose what you want to do: ")
                        graphs = analysis.Graphs(self.user_var, graph_menu, chosen_plot_type, self.user_nat, data)
                        graphs.graph_choice()
                case 3:
                    tests = analysis.StatisticsTest(data)
                    tests.choice()
                case 4:
                    file = files.Config(self.user_nat, self.user_var, self.user_date)
                    file.save_to_file()
                case _:
                    return True


if __name__ == "__main__":
    main = Main()
    while main.main_menu():
        pass
