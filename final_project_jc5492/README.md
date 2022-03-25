# final_project_jc5492

MDS final project jc5492

## Installation

```bash
$ pip install final_project_jc5492
```

## Usage

Parameters
----------
date : String <br>
  Either a single date in "YYYY-MM-DD" format, or a list of [min date, max date]<br>
time : String<br>
  Either a single time in "HH:MM" format, or a list of [min time, max time]<br>
zip_code : Integer<br>
  Either a single 5 digit zip code, or a list of [min zip code, max zip code]<br>
borough : String<br>
  List of boroughs to be included i.e. ["MANHATTAN","QUEENS","BRONX"]<br>
injury : Integer<br>
  Either a single integer or a list of [min injuries, max injuries]<br>
death : Integer<br>
  Either a single integer or a list of [min deaths, max deaths]<br>
limit : Integer <br>
  Maximum number of rows to return from API
  
Returns
--------
Pandas DataFrame<br>
 DataFrame of vehicle collisions returned from API
  
  Examples
  --------
 default_params = {"date":['2021-01-01','2021-01-15'],<br>
                              "time":["09:00","17:00" ],<br>
                              "borough":["MANHATTAN"],<br>
                              "injury":[0,10],<br>
                              "death":[0,0],<br>
                              "limit":10000}<br>
df = get_crash_data(default_params)


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`final_project_jc5492` was created by Jian Tong Chua. It is licensed under the terms of the MIT license.

## Credits

`final_project_jc5492` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
