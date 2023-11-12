import json
import os.path
from datetime import datetime

import pandas as pd
from github import Github


class Config:
    def __init__(self, user_nat, user_var, user_date):
        self.filename = "config.json"
        self.user_nat = user_nat
        self.user_var = user_var
        self.user_date = user_date

    def save_to_file(self):
        config = {"user_nationality": self.user_nat,
                  "user_variables": self.user_var,
                  "user_date": self.user_date.strftime("%Y-%m-%d %H:%M:%S")}
        with open(self.filename, mode="w", encoding="utf-8") as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r") as json_file:
                config = json.load(json_file)
                if config is not None:
                    user_nat = config.get("user_nationality", [])
                    user_var = config.get("user_variables", [])
                    user_date_str = config.get("user_date", "")
                    if "." in user_date_str:
                        user_date = datetime.strptime(user_date_str, "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        user_date = datetime.strptime(user_date_str, "%Y-%m-%d %H:%M:%S")
                    return user_nat, user_var, user_date
                else:
                    print("Unable to load configuration file")
                    return None
        except FileNotFoundError:
            print("File not found")
            return None
        except json.decoder.JSONDecodeError:
            print("Invalid JSON format, probably file is empty")
            return None


def download_or_update_covid_data():
    if os.path.isfile("covid_data.csv"):
        try:
            g = Github("token")
            commits = g.get_repo("owid/covid-19-data").get_commits(path="public/data/owid-covid-data.csv")
            last_commit_time = commits[0].commit.committer.date
            creation_time = datetime.fromtimestamp(os.path.getctime("covid_data.csv"))
            if last_commit_time > creation_time:
                os.remove("covid_data.csv")
                downloading_file_from_github()
            else:
                print("COVID-19 data is now up to date")
                del g, commits, last_commit_time, creation_time
        except BaseException as e:
            print(f"A GitHub authorization error occurred: {e} \n"
                  "The date cannot be updated")
            del g
    else:
        downloading_file_from_github()


def downloading_file_from_github():
    print("Downloading COVID-19 data...")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df.to_csv("covid_data.csv", index=False)
    print("COVID-19 data has been downloaded")
    del df
