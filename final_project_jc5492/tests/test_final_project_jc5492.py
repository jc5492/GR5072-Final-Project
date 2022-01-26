from final_project_jc5492 import final_project_jc5492 as final
import pytest


def test_min_max_date():
    default_params = {"date":['2021-01-15','2021-01-01'],
          "time":["09:00","17:00" ],
          "borough":["MANHATTAN"],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
    actual = final.get_crash_data(default_params).shape
    expected = (0,0)
    assert actual == expected


def test_min_max_time():
    default_params = {"date":['2021-01-01','2021-01-15'],
          "time":["15:00","08:00" ],
          "borough":["MANHATTAN"],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
    actual = final.get_crash_data(default_params).shape
    expected = (0,0)
    assert actual == expected


def test_date_format():
    default_params = {"date":['1st Jan 2020'],
          "time":["09:00","17:00" ],
          "borough":["MANHATTAN"],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
    actual = final.get_crash_data(default_params)
    expected = 400
    assert actual == expected
    

def test_zip_code():
    default_params = {"date":['2021-01-1','2021-01-15'],
          "time":["09:00","17:00" ],
          "borough":["MANHATTAN","Queens"],
          "zip_code":[1234567],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
    actual = final.get_crash_data(default_params)
    expected = 400
    assert actual == expected


def test_extra_params():
    default_params = {"date":['2021-01-1','2021-01-15'],
          "time":["09:00","17:00","23:00"],
          "borough":["MANHATTAN","Queens"],
          "zip_code":[1234567],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
    actual = final.get_crash_data(default_params)
    expected = "crash_time has to be list of either single time HH:MM or [min time, max time]"
    assert actual == expected   
