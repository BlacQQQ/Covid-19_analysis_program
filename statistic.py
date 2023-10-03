import matplotlib.pyplot as plt
import pandas as pd
from ydata_profiling import ProfileReport


class Statistic:
    pd.set_option("display.precision", 1)

    def __init__(self, user_nat, user_var, user_date, raw_df):
        self.user_var = user_var
        self.user_date = user_date
        self.raw_df = raw_df
        self.user_nat = user_nat

    def process_data(self):
        # list_of_df = []
        if len(self.user_nat) < 1:
            raise Exception("xd")
        filtered_df = self.raw_df.loc[(self.raw_df.index >= self.user_date) & (self.raw_df.index <= self.raw_df.index.max())]
        df_clear = filtered_df.dropna(how="all")
        for nat in self.user_nat:
            df_nat = pd.DataFrame(df_clear[df_clear['location'].str.contains(nat, na=False)])
            # list_of_df.append(df_nat[self.user_var])
            plt.plot(df_nat[self.user_var])
            plt.legend(self.user_nat)
        plt.title("xd")
        plt.show()


    # def long_report(self):
    #     profile = ProfileReport(self.df_clear, title="report")
    #     profile.to_file("report.json")
    #
    # def short_report(self):
    #     print(self.df_clear.describe())

    # def graphs(self):
    #     plt.plot(self.df_clear)
    #     plt.title("Plot Smooth Curve Using the scipy.interpolate.make_interp_spline() Class")
    #     plt.show()
