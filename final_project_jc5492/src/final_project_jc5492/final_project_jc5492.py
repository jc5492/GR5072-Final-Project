import requests
import pandas as pd
import geocoder

default_params = {"limit":10000}
		  
def get_crash_data(params=default_params):
  '''Gets vehicle collision data from NYC open data API based on provided dictionary of parameters.

  Parameters
  ----------
  date : String
    Either a single date in "YYYY-MM-DD" format, or a list of [min date, max date]
  time : String
    Either a single time in "HH:MM" format, or a list of [min time, max time]
  zip_code : Integer
    Either a single 5 digit zip code, or a list of [min zip code, max zip code]
  borough : String
    List of boroughs to be included i.e. ["MANHATTAN","QUEENS","BRONX"]
  injury : Integer
    Either a single integer or a list of [min injuries, max injuries]
  death : Integer
    Either a single integer or a list of [min deaths, max deaths]
  limit : Integer 
    Maximum number of rows to return from API
  
  Returns
  --------
  Pandas DataFrame
    DataFrame of vehicle collisions returned from API
  
  Examples
  --------
  >>> default_params = {"date":['2021-01-01','2021-01-15'],
          "time":["09:00","17:00" ],
          "borough":["MANHATTAN"],
          "injury":[0,10],
          "death":[0,0],
          "limit":10000}
  >>> df = get_crash_data(default_params)

  '''
  endpoint = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$where="
  filters = []
  #add crash_date_filter
  if "date" not in params:
    datefilter = ""
  elif len(params["date"])==1:
    datefilter = "crash_date=" + "'" + params["date"][0] + "'"
    filters.append(datefilter)
  elif len(params["date"])==2:
    datefilter = "crash_date " + "between '" + params["date"][0] + "' and '" + params["date"][1] + "'"
    filters.append(datefilter)
  else:
    return "crash_date has to be list of either single date YYYY-MM-DD or [min date, max date]"

  #add crash_time filter
  if "time" not in params:
    timefilter=""
  elif len(params["time"])==1:
    timefilter = "crash_time=" + "'" + params["time"][0] + "'"
    filters.append(timefilter)
  elif len(params["time"])==2:
    timefilter = "crash_time " + "between '" + params["time"][0] + "' and '" + params["time"][1] + "'"
    filters.append(timefilter)
  else:
    return "crash_time has to be list of either single time HH:MM or [min time, max time]"

  #add zip_code filter
  if "zip_code" not in params:
    zipfilter=""
  elif len(params["zip_code"])==1:
    zipfilter = "zip_cide=" + "'" + str(params["zip_code"][0]) + "'"
    filters.append(zipfilter)
  elif len(params["zip_code"])==2:
    zipfilter = "zip_code " + "between '" + str(params["zip_code"][0]) + "' and '" + str(params["zip_code"][1]) + "'"
    filters.append(zipfilter)
  else:
    return "zip_code has to be list of either single zipcode (5 digits) or [min zipcode, max zipcode]"

  #add injury filter
  if "injury" not in params:
    injuryfilter=""
  elif len(params["injury"])==1:
    injuryfilter = "number_of_persons_injured=" + "'" + str(params["injury"][0]) + "'"
    filters.append(injuryfilter)
  elif len(params["injury"])==2:
    injuryfilter = "number_of_persons_injured " + "between '" + str(params["injury"][0]) + "' and '" + str(params["injury"][1]) + "'"
    filters.append(injuryfilter)
  else:
    return "injury has to be list of either single number or [min injuries, max injuries]"

  #add death filter
  if "death" not in params:
    deathfilter=""
  elif len(params["death"])==1:
    deathfilter = "number_of_persons_killed=" + "'" + str(params["death"][0]) + "'"
    filters.append(deathfilter)
  elif len(params["death"])==2:
    deathfilter = "number_of_persons_killed " + "between '" + str(params["death"][0]) + "' and '" + str(params["death"][1]) + "'"
    filters.append(deathfilter)
  else:
    return "injury has to be either single number or [min deaths, max deaths]"

  #add borough filter
  if "borough" not in params:
    boroughfilter=""
  else:
    boroughfilter="("
    for b in range(0, len(params['borough'])):
      if b == len(params['borough'])-1:
        boroughfilter = boroughfilter + "borough='" + params['borough'][b].upper() + "')"
      else:
        boroughfilter = boroughfilter + "borough='" + params['borough'][b].upper() + "' OR "
    filters.append(boroughfilter)

  #add limit
  if "limit" not in params:
    limit=""
  else:
    limit="&$limit="+str(params['limit'])


  query = endpoint
  for filter in filters:
    if filter == filters[0]:
      query = query + filter
    else:
      query = query + " and " + filter
  query = query + limit

  r=requests.get(query)
  if r.status_code == 200:
    df = pd.DataFrame(r.json())
    return df
  else:
    return r.status_code

def geocode_missing_row(row):
  '''Geocodes on/off/cross street names  and zip codes to return latitude and longitude

  Parameters
  ----------
  row: Row of a Dataframe
    Contains columns for "on_street_name", "off_street_name", "cross_street_name" and "zip_code"
  
  Returns
  --------
  List
    List of geocoded coordinates [lat,long]
  
  '''
  if pd.notnull(row['cross_street_name']):
    if geocoder.osm(row['cross_street_name'] + " " + row['borough'] + " New York " + str(row['zip_code'])).latlng is not None:
      return geocoder.osm(row['cross_street_name'] + " " + row['borough'] + " New York " + str(row['zip_code'])).latlng
    else:
      return [None,None]
  elif geocoder.osm(str(row['on_street_name'])+ " " + str(row['off_street_name'])).latlng is not None:
    return geocoder.osm(str(row['on_street_name']) + " " + str(row['off_street_name'])).latlng
  elif geocoder.osm(str(row['off_street_name']) + " " + str(row['on_street_name'])).latlng is not None:
    return geocoder.osm(str(row['off_street_name']) + " " + str(row['on_street_name'])).latlng
  else:
    return [None,None]
