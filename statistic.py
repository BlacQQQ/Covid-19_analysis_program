from datetime import datetime


def statistical_analysis(chosen_nat, args, raw_df, index_date):
    df = raw_df[args].loc[raw_df["location"].str.contains(chosen_nat)]
    df2 = df.loc[str(index_date):str(datetime.now())]
    df_clear = df2.dropna(how="all")
    print(df_clear.to_string())
