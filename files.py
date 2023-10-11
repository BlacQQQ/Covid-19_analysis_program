import json
import os.path
from datetime import datetime

import pandas as pd
from github import Github


class Config:
    def __init__(self, user_nat, user_var, user_date):
        self.config = {"user_nationality": user_nat,
                       "user_variables": user_var,
                       "user_date": str(user_date)}

    def save_config_to_file(self):
        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(self.config, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_config_from_file():
        try:
            with open("config.json", "r") as json_file:
                config = json.load(json_file)
            return config
        except FileNotFoundError:
            print("Nie znaleziono pliku")
            return None

    @staticmethod
    def extract_config(config):
        user_nat = config.get("user_nationality", [])
        user_var = config.get("user_variables", [])
        user_date_str = config.get("user_date", "")
        user_date = None
        if user_date_str:
            user_date = datetime.strptime(user_date_str, "%Y-%m-%d %H:%M:%S")
        return user_nat, user_var, user_date


def download_or_update_covid_data():
    if os.path.isfile("covid_data.csv"):
        g = Github("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")
        repo = g.get_repo("owid/covid-19-data")
        commits = repo.get_commits(path="public/data/owid-covid-data.csv")
        last_commit_time = commits[0].commit.committer.date
        creation_time = datetime.fromtimestamp(os.path.getctime("covid_data.csv"))
        if last_commit_time > creation_time:
            os.remove("covid_data.csv")
            downloading_file_from_github()
        else:
            print("Dane COVID-19 są już aktualne.")
    else:
        downloading_file_from_github()


def downloading_file_from_github():
    print("Pobieranie danych COVID-19...")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df.to_csv("covid_data.csv", index=False)
    print("Dane COVID-19 zostały pobrane.")
