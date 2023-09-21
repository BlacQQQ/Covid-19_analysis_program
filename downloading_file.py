import os.path
from datetime import datetime

import pandas as pd
from github import Auth
from github import Github


def downloading_file_from_github():
    token = Auth.Token("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")
    if os.path.isfile("covid_data.csv"):
        g = Github(auth=token)
        commits = g.get_repo("owid/covid-19-data").get_commits(path="public/data/owid-covid-data.csv")
        time_of_last_commit = commits[0].commit.committer.date
        creation_time_od_csv_file = datetime.fromtimestamp(os.path.getctime("covid_data.csv"))
        if time_of_last_commit > creation_time_od_csv_file:
            print("Aktuazlizacja bazy danych... Prosze czekac")
            os.remove("covid_data.csv")
            url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
            df = pd.read_csv(url)
            df.to_csv("covid_data.csv", index=False)
            print("Pobieranie zakonczone")
            del df
        else:
            pass
    else:
        print("Pobieranie bazy danych... Prosze czekac")
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        df = pd.read_csv(url)
        df.to_csv("covid_data.csv", index=False)
        print("Pobieranie zakonczone")
        del df
