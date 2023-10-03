from datetime import datetime, date

from dateutil.relativedelta import relativedelta


class DataMenu:
    last_2_weeks = 1
    last_month = 2
    last_3_months = 3
    last_half_year = 4
    last_year = 5
    all_time = 6
    custom_time = 7

    def __init__(self, raw_df):
        self.start_date = raw_df.index.min()
        self.end_date = raw_df.index.max()

    def index_range(self):
        print("1. z 2 ostatnich tygodni")
        print("2. z ostatniego miesiaca")
        print("3. z ostatnich 3 miesiecy")
        print("4. z ostatniego pol roku")
        print("5. z ostatniego roku")
        print("6. caly okres dostepy w bazie")
        print("7. zakres customowy")
        user_input = int(input("Podaj z jakiego okresu czasu maja zostac przeanalizowane dane: "))
        match user_input:
            case self.last_2_weeks:
                return datetime.now() - relativedelta(days=14)
            case self.last_month:
                return datetime.now() - relativedelta(months=1)
            case self.last_3_months:
                return datetime.now() - relativedelta(months=3)
            case self.last_half_year:
                return datetime.now() - relativedelta(months=6)
            case self.last_year:
                return datetime.now() - relativedelta(years=1)
            case self.all_time:
                user_date = self.start_date
                return user_date
            case self.custom_time:
                self.get_custom_date()

    def get_custom_date(self):
        while True:
            date_components = input("Podaj date w formacie YYYY-MM-DD: ").split("-")
            year, month, day = [int(item) for item in date_components]
            user_date = date(year, month, day)
            if user_date < self.start_date or user_date > self.end_date:
                print(
                    f"Podany zakres daty nie miesci sie w zakresie bazy danych, minimalny zakres to {self.start_date}, maksymalny to {self.end_date}")
            else:
                return user_date
