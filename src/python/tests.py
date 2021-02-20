import data_model as dm
import os, sys, inspect
import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
data_reader = dm.data_model(parentdir + "/data/raw")


def test_get_timeserie_data_by_country():
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date.today()
    results = data_reader.get_timeserie_data_by_country(
        country="all", c_type=1, start_date=start_date, end_date=end_date
    )
    assert len(results) > 0, "Invalid result"


def test_all():
    test_get_timeserie_data_by_country()
