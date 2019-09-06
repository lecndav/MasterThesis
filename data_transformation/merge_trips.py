import argparse
import pathlib
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import DateFormatter
import numpy as np
from asammdf import MDF
import csv
import glob

import os
import sys


def get_trips(input_path):
  driver = dict()
  trips = dict()
  max_trip_delta = 5 * 60 * 1000000000  # 5 minutes
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    timestamp = file.split('_')[0]
    if id not in driver:
        driver[id] = []
    driver[id].append(timestamp)

  for d in driver:
    driver[d].sort()
    new_trip = True
    trips[d] = []
    tlast = float(driver[d][0])
    for ts in driver[d]:
      t = float(ts)
      if new_trip:
        trips[d].append([])
        new_trip = False
      if (t - tlast) > max_trip_delta:
        tlast = t
        new_trip = True
      else:
        trips[d][-1].append(ts)
        tlast = t
  return trips


def get_signal_groups(input_path):
  file = os.listdir(input_path)[0]
  mdf_file = MDF(os.path.join(input_path, file))
  info = mdf_file.info()
  group_count = info['groups']
  groups = []
  for i in range(0, group_count):
    group = info['group %d' % i]
    groups.append(group['comment'])
    
  return groups


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-c', '--csv-input',
                         action='store',
                         metavar='csv_input',
                         type=str,
                         required=True,
                         help='Input csv file or directory')

  my_parser.add_argument('-m', '--mf4-input',
                         action='store',
                         metavar='mf4_input',
                         type=str,
                         required=True,
                         help='Input mf4 file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  csv_input_path = args.csv_input
  mf4_input_path = args.mf4_input

  if not os.path.isdir(csv_input_path):
    print('The csv input path specified is not a directory')
    sys.exit()

  if not os.path.isdir(mf4_input_path):
    print('The mf4 input path specified is not a directory')
    sys.exit()

  trips = get_trips(mf4_input_path)
  groups = get_signal_groups(mf4_input_path)
  for d in trips:
    for trip in trips[d]:
      for group in groups:
        merged_csv = open(os.path.join('trips', '%s_%s_%s.csv' % (trip[0], d, group)), mode='w')
        merged_csv_writer = csv.writer(merged_csv, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for t in trip:
          source_name = os.path.join(csv_input_path, ('%s_%s*_%s*.csv' % (t, d, group)))
          source_file = glob.glob(source_name)[0]
          source_csv = open(source_file)
          csv_reader = list(csv.reader(source_csv, delimiter=','))
          if t == trip[0]:
            merged_csv_writer.writerow(csv_reader[0])
          for row in csv_reader[1:]:
            ts = float(row[0]) * 1000000000 + float(t)
            row[0] = '%.0f' % ts
            merged_csv_writer.writerow(row)
          source_csv.close()
        merged_csv.close()
            


if __name__ == "__main__":
  main()
