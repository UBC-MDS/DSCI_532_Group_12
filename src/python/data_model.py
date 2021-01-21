import pandas as pd
import datetime
import os, sys, inspect
import numpy as np

file_daily_report = "daily_report.csv"
file_timeseries_confirmed = "time_series_covid19_confirmed_global.csv"
file_timeseries_recovered = "time_series_covid19_recovered_global.csv"
file_timeseries_death = "time_series_covid19_deaths_global.csv"


class case_type:
    all = 0
    confirmed = 1
    death = 2
    recovered = 3


class data_model:
    """handles data reading and processing"""

    def __init__(self, path):
        self.data_path = path
        self.reload()
        self.country_list = self.daily_report.Country_Region.unique()

    def reload(self):
        """load the csv files into data frame, download the files from Github if needed"""
        today = datetime.date.today()
        today = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        m_day = self.__get_modified_date()

        # check if the data is old
        if m_day < today:
            # we need to re-download data
            self.__download_data(today)

        # process the data
        self.__process_data()

    def __download_data(self, date):
        """private method, used for downloading files from github of JH Uni

        Args:
            date (datetime): date to retrieve daily report
        """
        # download daily report
        # we need to handle time zone difference, first check if there is a file created for our today, then 1, 2 day before
        dr_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports"
        yesterday = date - datetime.timedelta(days=1)
        bf_yesterday = yesterday - datetime.timedelta(days=1)

        dr_files = [
            self.__create_filename(date),
            self.__create_filename(yesterday),
            self.__create_filename(bf_yesterday),
        ]
        for f in dr_files:
            try:
                url = dr_path + "/" + f
                input = pd.read_csv(url)
                input.to_csv(self.data_path + "/" + file_daily_report)
                break  # as we sorted the date desc, we just need to get the latest file
            except:
                next

        # download timeseries
        ts_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
        ts_files = [
            file_timeseries_confirmed,
            file_timeseries_death,
            file_timeseries_recovered,
        ]
        for f in ts_files:
            url = ts_path + "/" + f
            input = pd.read_csv(url)
            input.to_csv(self.data_path + "/" + f)

    def __create_filename(self, date):
        """private method, generates file name for daily report from date

        Args:
            date (datetime): any date to get the daily report file name

        Returns:
            string: mm-dd-year.csv
        """
        return f"{format(date.month, '02d')}-{format(date.day, '02d')}-{date.year}.csv"

    def __get_modified_date(self):
        """get the daily report's modified date, returns 1990-01-01 if the file does not exist

        Returns:
            datetime: modified date
        """
        daily_r = self.data_path + "/" + file_daily_report
        dirpath = os.path.dirname(daily_r)
        if not os.path.exists(daily_r):
            return datetime.datetime(1990, 1, 1, 0, 0)

        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(daily_r))
        modified_date = datetime.datetime(
            modified_date.year, modified_date.month, modified_date.day, 0, 0, 0
        )
        return modified_date

    def __process_data(self):
        """private method, used for reading and cleaning up data files"""
        # read the files in as data frame
        self.daily_report = pd.read_csv(self.data_path + "/" + file_daily_report)
        self.times_series_confirmed = pd.read_csv(
            self.data_path + "/" + file_timeseries_confirmed
        )
        self.times_series_death = pd.read_csv(
            self.data_path + "/" + file_timeseries_death
        )
        self.times_series_recovered = pd.read_csv(
            self.data_path + "/" + file_timeseries_recovered
        )

        # clean up data frames as needed

    def get_aggregated_daily_report(self):
        """ Aggregate the regional level cases count to country level"""
        return self.daily_report.groupby(
            'Country_Region'
        ).agg(
            {'Confirmed': 'sum',  'Deaths': 'sum', 'Recovered': 'sum', 'Active': 'sum'}
        ).reset_index()

    def cumulative_filter(self, country="all"):
        """return cumulative cases by country

        Args:
            country (str, optional): [description]. Defaults to "all".

        Returns:
            [Series]: with index as Confirmed, Deaths, Recovered
        """
        if country != "all":
            return self.daily_report.query(f"Country_Region == '{country}'").sum(
                numeric_only=True
            )

        return self.daily_report.sum(numeric_only=True)

    def get_country_options(self):
        """create an array of country options to be used in dropdowns

        Returns:
            array: [{"label":country1, "value":country1}, ...]
        """
        result = []
        for i in range(len(self.country_list)):
            result.append(
                {"label": self.country_list[i], "value": self.country_list[i]}
            )

        return result


    def get_timeserie_data_by_country(self, country="all", c_type=case_type.confirmed):
        """return timeseries data by country

        Args:
            country (str, optional): country name. Defaults to "all".
            case_type (int, optional): 1: confirmed, 2: death, 3: recovered. Defaults to case_type.confirmed.

        Raises:
            Exception: if case_type entered is invalid
        Return:
            country_data: DataFrame, date: date, total: total number, yesterday: the day before's number, new: total - yesterday
        """
        if c_type == case_type.confirmed:
            df = self.times_series_confirmed
        elif c_type == case_type.death:
            df = self.times_series_death
        elif c_type == case_type.recovered:
            df = self.times_series_recovered
        else:
            raise Exception("Case type is not supported")
        if country != "all":
            country_data = pd.DataFrame(
                df[df["Country/Region"] == country].iloc[:, 5:].sum()
            )
        else:
            country_data = pd.DataFrame(df.iloc[:, 5:].sum())
        country_data = country_data.reset_index()
        country_data.columns = ["date", "Total"]
        yesterday_data = np.zeros(country_data.Total.shape[0])
        yesterday_data[1:] = country_data.Total.to_numpy()[0:-1]
        country_data["yesterday"] = yesterday_data
        country_data["New"] = country_data.Total - country_data["yesterday"]

        country_data = country_data.loc[:, ["date", "Total", "New"]]
        country_data = pd.melt(
            country_data,
            id_vars=["date"],
            value_vars=["Total", "New"],
            value_name="count",
            var_name="type",
        )

        return country_data

    def save_to_file(self):
        """save the whole data model into file"""
        pass
