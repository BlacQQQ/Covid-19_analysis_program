import json

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from scipy.stats import shapiro, ttest_ind
from ydata_profiling import ProfileReport

import user_input


class Data:
    def __init__(self, user_nat, user_var, user_date, raw_df):
        self.user_var = user_var
        self.user_date = user_date
        self.raw_df = raw_df
        self.user_nat = user_nat
        self.df = None
        self.df_list = []
        self.filtered_df = None

    def filtered(self):
        date_filtered_df = self.raw_df.loc[
            (self.raw_df.index >= self.user_date) & (self.raw_df.index <= self.raw_df.index.max())]
        df_cleared = date_filtered_df.dropna(how="all")
        for nat in self.user_nat:
            nat_filtered_df = pd.DataFrame(df_cleared[df_cleared['location'].str.contains(nat)])
            self.filtered_df = nat_filtered_df[self.user_var]
            if not self.filtered_df.empty:
                self.df_list.append(self.filtered_df)
            else:
                print(f"Cannot create df for {nat}")


class Reports:
    def __init__(self, user_nat, user_var, data: Data):
        self.df_list = data.df_list
        self.user_nat = user_nat
        self.user_var = user_var

    def generate(self):
        list_of_report_names = []
        for df, nat in zip(self.df_list, self.user_nat):
            print(f"Statistical description for {nat}")
            print(df.describe())
            user_choice = user_input.str_input("Do you want to generate a full report? (Yes/No): ").strip().lower()
            if user_choice.lower() == "yes":
                report_name = f"Report_for_{nat.replace(' ', '_')}"
                list_of_report_names.append(report_name)
                profile = ProfileReport(df, title=report_name)
                profile.to_file(f"{report_name}.json")
                user_choice = user_input.str_input("Do you want to load the resulting report? (Yes/No): ")
                if user_choice == "yes":
                    self.read(report_name)
                elif user_choice == "no":
                    pass
            elif user_choice.lower() == "no":
                pass
            else:
                print("Please enter yes or no")
        if len(list_of_report_names) >= 1:
            return list_of_report_names

    def read(self, selected_report_name):
        try:
            with open(selected_report_name, "r") as json_file:
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
                                    print(f"The {var_name} variable is not a dictionary type")
                            else:
                                print(f"Variable {var_name} does not exist in the report")
                    elif section_name == "correlations":
                        if isinstance(section_data, dict):
                            for correlation_key, correlation_list in section_data.items():
                                if isinstance(correlation_list, list):
                                    for correlation_data in correlation_list:
                                        if isinstance(correlation_data, dict):
                                            for i, (key, value) in enumerate(correlation_data.items(), start=1):
                                                if key not in keys_to_exclude:
                                                    print(f"{i}. {key}: {value}")
                                        else:
                                            print(f"Unsupported data type in section {section_name}")
                                else:
                                    print(f"The {section_name} section is not a list type")
                        else:
                            print(f"The {section_name} section is not a dictionary type")
                    else:
                        if isinstance(section_data, dict):
                            for i, (key, value) in enumerate(section_data.items(), start=1):
                                if key not in keys_to_exclude:
                                    print(f"{i}. {key}: {value}")
                        else:
                            print(f"Unsupported data type in section {section_name}")
                else:
                    print(f"The {section_name} section does not exist in the report")
        except FileNotFoundError:
            print("Report file not found")


class Graphs:
    def __init__(self, user_var, graph_menu, chosen_plot_type, user_nat, data: Data):
        self.user_var = user_var
        self.graph_menu = graph_menu
        self.chosen_plot_type = chosen_plot_type
        self.user_nat = user_nat
        self.df_list = data.df_list

    def graph_choice(self):
        if self.graph_menu == 1:
            for df, nat in zip(self.df_list, self.user_nat):
                for var in self.user_var:
                    self.generate_plot(df, nat, var)
        elif self.graph_menu == 2:
            for df, nat in zip(self.df_list, self.user_nat):
                self.generate_plot(df, nat)

    @staticmethod
    def configure(ax):
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.legend()

    def generate_plot(self, df, nat, var=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        if self.graph_menu == 1:
            data = df[var]
            plt.title(f"Graph of {var} for {nat}")
        else:
            data = df
            plt.title(f"Graph of {', '.join(self.user_var)} for {nat}")
        if self.chosen_plot_type == "Line Plot":
            if self.graph_menu == 2:
                for user_var in self.user_var:
                    ax.plot(df.index, data[user_var], label=f"{nat}, {user_var}")
            else:
                ax.plot(df.index, data, label=f"{nat}, {var}")
            ax.legend()
            plt.show()
        elif self.chosen_plot_type == "Bar Plot":
            print("work in progress")
            # ax.bar(df.index, data, label=f"{nat}, {var}")
        elif self.chosen_plot_type == "Horizontal Bar Plot":
            print("work in progress")
            # ax.barh(df.index, data, label=f"{nat}, {var}")
        elif self.chosen_plot_type == "Grouped Bar Plot":
            print("work in progress")
        #     categories = df.index
        #     width = 0.35
        #     ax.bar(categories - width / 2, data, width, label=f"{nat}, {var}")
        # self.configure(ax)
        # plt.show()


class StatisticsTest:
    def __init__(self, data: Data):
        self.df_list = data.df_list
        self.user_nat = data.user_nat

    def choice(self):
        user_choice = user_input.int_input("1. Normality test \n"
                                           "2. Chi-Squared Test \n"
                                           "3. T-student test \n"
                                           "4. Paired Student’s t-test \n"
                                           "5. Analysis of Variance Test (ANOVA) \n"
                                           "6. Repeated Measures ANOVA Test \n"
                                           "Choose what you want to do: ")
        match user_choice:
            case 1:
                self.normality_test()
            case 2:
                self.chi_squared_test()
            case 3:
                self.t_student_test()
            case 4:
                self.paired_students_test()
            case 5:
                self.anova()
            case 6:
                self.repeated_anova()

    def normality_test(self):
        for country, df in zip(self.user_nat, self.df_list):
            print(f"Normality test for data from {country}:")
            for column in df.columns:
                try:
                    stat, p = shapiro(df[column])
                    if not pd.isna(stat):
                        print(f"Column: {column}")
                        print(f"stat=%.5f, p=%.5f" % (stat, p))
                        if p > 0.05:
                            print('Probably Gaussian')
                        else:
                            print('Probably not Gaussian')
                    else:
                        print(f"Unable to calculate the normality test for {country}, {column}")
                except Exception as e:
                    print(f"An error occurred while calculating the normality test for {country}, {column}: {e}")

    def chi_squared_test(self):
        print("work in progress")
        # table = [[10, 20, 30], [6, 9, 17]]
        # stat, p, dof, expected = chi2_contingency(table)
        # print('stat=%.3f, p=%.3f' % (stat, p))
        # if p > 0.05:
        #     print('Probably independent')
        # else:
        #     print('Probably dependent')
        pass

    def t_student_test(self):
        for country, df in zip(self.user_nat, self.df_list):
            print(f"Normality test for data from {country}:")
            stat, p = ttest_ind(df.c, df)
            print('stat=%.3f, p=%.3f' % (stat, p))
            if p > 0.05:
                print('Probably the same distribution')
            else:
                print('Probably different distributions')
            pass

    def paired_students_test(self):
        print("work in progress")
        pass

    def anova(self):
        print("work in progress")
        pass

    def repeated_anova(self):
        print("work in progress")
        pass
