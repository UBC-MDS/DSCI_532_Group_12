import pandas as pd

file_daily_report = "data/raw/daily_report.csv"
file_timeseries_confirmed = "data/raw/time_series_covid19_confirmed_global.csv"
file_timeseries_recovered = "data/raw/time_series_covid19_recovered_global.csv"
file_timeseries_death = "data/raw/time_series_covid19_deaths_global.csv"


class case_type:
    all = 0
    confirmed = 1
    death = 2
    recovered = 3


class country_code:
    pass


class data_model:
    """handles data reading and processing"""

    def __init__(self):
        self.__process_data()

    def reload(self):
        self.__process_data()

    def __process_data(self):
        """private method, used for reading and cleaning up data files"""
        # read the files in as data frame
        self.daily_report = pd.read_csv(file_daily_report)
        self.times_series_confirmed = pd.read_csv(file_timeseries_confirmed)
        self.times_series_death = pd.read_csv(file_timeseries_death)
        self.times_series_recovered = pd.read_csv(file_timeseries_recovered)

        # clean up data frames as needed

    def cumulative_filter(self, country=0, case_type=case_type.all):
        """return cumulative case number by country and case type
        Args:
            case_type (integer): 0: all, 1: confirmed, 2: death, 3: recovered. Defaults to 0.
            country (int, optional): country code. Defaults to 0 (all countries)
        """
        pass

    def timeseries_filter(self, country=0, case_type=case_type.confirmed):
        """return timeserie data for a country with case type

        Args:
            country (int, optional): [description]. Defaults to 0.
            case_type ([type], optional): [description]. Defaults to case_type.confirmed.
        """
        pass

    def save_to_file(self):
        """save the whole data model into file"""
        pass