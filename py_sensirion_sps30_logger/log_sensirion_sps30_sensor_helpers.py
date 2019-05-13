# Load modules
import time, datetime, pytz
from math import floor
from collections import OrderedDict
import csv
import os
import json
import argparse
import pys_logging_helpers

# Define some helpers
def write_sensor_dict_to_csv(dict, file):
  # Create file, write header and write row
  if not os.path.isfile(file): 
    with open(file, "wb") as f:
      w = csv.DictWriter(f, dict.keys())
      w.writeheader()
      w.writerow(dict)
  
  # Just write row
  else: 
    with open(file, "a") as f:
      w = csv.DictWriter(f, dict.keys())
      w.writerow(dict)


def get_sensirion_sps30_data(sensor, time_zone, names):

  # Get measurement date
  date = time.time()
  
  # Used for logging and other data export things but not logic
  date_floor = floor(date)
  
  # Make a date string
  date_string = datetime.datetime.fromtimestamp(
    date_floor,
    pytz.timezone(time_zone)
  ).strftime("%Y-%m-%d %H:%M:%S %Z")
  
   # Create an extra dictionary
  dict_dates = OrderedDict([
    ('date', date_string),
    ('date_unix', date_floor)
  ])
  
  if sensor is None: 
    # Example response
    response = (-99.9, -99.9, -99.9, -99.9, -99.9, -99.9, -99.9, -99.9, -99.9, -99.9)

  else: 
    # Query sensor
    response = sensor.read_values()

  # Create a dictionary
  dict_results = dict(zip(names, response))
  
  # Bind dictionaries
  dict_results = OrderedDict(
    list(dict_dates.items()) + 
    list(dict_results.items())
  )
  
  # Arrange variables 
  names_with_dates = ["date", "date_unix"] + names

  dict_results = OrderedDict(
    sorted(
      dict_results.items(), 
      key = lambda pair: names_with_dates.index(pair[0])
    )
  )

  return dict_results


def summarise_sensirion_sps30_data(list_results, digits, names, 
  verbose = False): 

  # Create an extra dictionary, use first dates
  dict_dates = OrderedDict([
    ('date', list_results[0]["date"]),
    ('date_unix', list_results[0]["date_unix"])
  ])

  # Remove dates from dictionary for aggregation
  for d in list_results:
    d.pop("date", None)
    d.pop("date_unix", None)

  # Get n
  count = float(len(list_results))

  # sum / count
  dict_results_summary = {
    k:sum(t[k] for t in list_results) / count for k in list_results[0]
  }

  # Round values
  dict_results_summary = {
    k:round(v, digits) for k, v in dict_results_summary.items()
  }

  # Bind dictionaries
  dict_results_summary = OrderedDict(
    list(dict_dates.items()) + 
    list(dict_results_summary.items())
  )
    
  # Arrange variables 
  names_with_dates = ["date", "date_unix"] + names

  dict_results_summary = OrderedDict(
    sorted(
      dict_results_summary.items(), 
      key = lambda pair: names_with_dates.index(pair[0])
    )
  )
    
  # Print
  if verbose: 
    print(json.dumps(dict_results_summary, indent = 2))

  return dict_results_summary


def catch_arguments(): 
  
  # Command line arguments
  parser = argparse.ArgumentParser()
  
  # The arguments
  parser.add_argument(
    "-o", 
    "--output", 
    default = "~/Desktop/data", 
    help = "Which directory should be used to export the programme's data files \
    too?"
  )
  
  parser.add_argument(
    "-d", 
    "--device", 
    default = "/dev/ttyUSB0", 
    help = "What is the device/location is the Sensirion SPS30 sensor?"
  )
  
  parser.add_argument(
    "-tz", 
    "--time_zone", 
    default = "UTC",
    help = "Which time zone will the date be stored in? As an Olison time-zone \
    string. Epoch time is also stored so time-zone information can always be \
    found from the data files."
  )
  
  # Add arguments to object to be called in programme
  args = parser.parse_args()
  
  # Modify file directory so ~ can be used  
  args.output = os.path.expanduser(args.output)
  
  # If the output directory does not exist, create it
  pys_logging_helpers.create_directory(args.output)
  
  return args
