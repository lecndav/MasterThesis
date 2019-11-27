import argparse
import pathlib
from datetime import datetime
import numpy as np
import glob
from asammdf import MDF

import os
import sys


def print_ids(input_path):
  print('=====Driver IDs=====')
  ids = []
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    if id not in ids:
      ids.append(id)

  print('\n'.join(ids))
  print('count: %d' % len(ids))

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


def print_drive_time(trips):
  print('=====Drive time====')
  total = 0
  trip_count = 0
  for d in trips:
    count = 0
    trip_count += len(trips[d])
    for t in trips[d]:
      count += len(t)
    print('%s: Total: %d, Average: %d, Count: %d' % (d, count, count / len(trips[d]), len(trips[d])))
    total += count

  print('Total: %d, Average: %d, Count: %d' % (total, total / len(trips), trip_count))

def print_trips(trips):
  print('=====Trips=====')
  trip_count = 0
  total = 0
  for d in trips:
    count = 0
    trip_count += len(trips[d])
    for t in trips[d]:
      count += len(t)
    print('%s: %d' % (d, len(trips[d])))
    total += count / len(trips[d])
  print('Total: %d, Average: %d, Trip time average: %d' % (trip_count, trip_count / len(trips), total / len(trips)))


def print_dates(trips):
  print('=====Dates=====')
  dates = []
  for d in trips:
    start = int(trips[d][0][0]) / 1000000000
    end = int(trips[d][-1][-1]) / 1000000000
    dates.append(start)
    dates.append(end)
    start_date = datetime.fromtimestamp(start).strftime('%d.%m.%Y')
    end_date = datetime.fromtimestamp(end).strftime('%d.%m.%Y')
    print('%s: %s - %s' % (d, start_date, end_date))
  dates.sort()
  first = datetime.fromtimestamp(dates[0]).strftime('%d.%m.%Y')
  last = datetime.fromtimestamp(dates[-1]).strftime('%d.%m.%Y')
  print('Time range: %s - %s' % (first, last))


def print_km(trips, dir):
  print('=====KM=====')
  total = 0
  for d in trips:
    first = trips[d][0][0]
    last = trips[d][-1][-1]
    first = os.path.join(dir, '%s_%s.mf4' % (first, d))
    last = os.path.join(dir, '%s_%s.mf4' % (last, d))
    delta = get_km(last) - get_km(first)
    total += delta
    print('%s: %d' % (d, delta))
  print('Total: %d, Average: %d' % (total, total / len(trips)))

def get_km(file):
  mdf = MDF(file)
  sig = mdf.get('can0_KBI_Kilometerstand_2')
  for s in list(sig.samples):
    if s != 0:
      return s

def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-m', '--mf4-input',
                         action='store',
                         metavar='mf4_input',
                         type=str,
                         required=True,
                         help='Input mf4 file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()
  mf4_input_path = args.mf4_input

  if not os.path.isdir(mf4_input_path):
    print('The mf4 input path specified is not a directory')
    sys.exit()

  trips = get_trips(mf4_input_path)
  print_ids(mf4_input_path)
  print_trips(trips)
  print_drive_time(trips)
  print_dates(trips)
  print_km(trips, mf4_input_path)


if __name__ == "__main__":
  main()
