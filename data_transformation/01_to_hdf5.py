import argparse
import pathlib
import pandas
import os
import sys
from datetime import datetime
from asammdf import MDF


def order_files(input_path):
  driver = dict()
  for file in os.listdir(input_path):
    if file.split('.')[-1] != 'mf4':
      continue
    id = file.split('_')[1].split('.')[0]
    timestamp = file.split('_')[0]
    if id not in driver:
        driver[id] = []
    driver[id].append(timestamp)

  for id in driver:
    driver[id].sort()

  return driver


def get_trips(driver):
  trips = dict()
  max_trip_delta = 5 * 60 * 1000000000  # 5 minutes
  for d in driver:
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


def to_hdf5(ts, id, mf4_dir, hdf_dir):
  hdf_file = os.path.join(hdf_dir, '%s.hdf' % id[:5])
  for t in ts:
    file = os.path.join(mf4_dir, '%s_%s.mf4' % (t, id))
    mdf_file = MDF(file)
    data = mdf_file.to_dataframe()
    data.index = (data.index * 1000000000 + float(t))
    data.index = data.index.values.astype('datetime64[ns]')
    data.index = pandas.to_datetime(data.index)
    data.to_hdf(hdf_file, id.replace('-', '_'), append=True)


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-m', '--mdf-input',
                         action='store',
                         metavar='mdf_input',
                         type=str,
                         required=True,
                         help='Input mdf file or directory')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='ouput',
                         type=str,
                         required=True,
                         help='HDF5 dir to write')
  
  my_parser.add_argument('-d', '--duration',
                         action='store',
                         metavar='duration',
                         type=int,
                         required=False,
                         help='Duration in minutes')

  my_parser.add_argument('-t', '--trips',
                         action='store',
                         metavar='trips',
                         type=int,
                         required=False,
                         help='Trip count')

  my_parser.add_argument('--offset',
                          action='store',
                          metavar='offset',
                          type=str,
                          required=False,
                          help='Offset for either trips (count) or duration (time [m])')
  
  my_parser.add_argument('-id', '--ids',
                         action='store',
                         metavar='ids',
                         type=int,
                         required=False,
                         help='Amount of included IDs')


  # Execute the parse_args() method
  args = my_parser.parse_args()

  mdf_input_path = args.mdf_input
  hdf_dir = args.output
  duration = None
  trip_count = None
  offset = 0
  if args.duration:
    duration = int(args.duration)
  elif args.trips:
    trip_count = int(args.trips)
  else:
    print('Either sepcifiy duration or amount of trips')
    sys.exit(1)

  if args.offset:
    offset = args.offset

  if not os.path.isdir(mdf_input_path):
    print('The mdf input path specified is not a directory')
    sys.exit()

  files = order_files(mdf_input_path)
  trips = get_trips(files)

  i = 0
  l = len(trips)
  if args.ids:
    l = args.ids
  for id in trips:
    i += 1
    if i == l:
      break
    if duration:
      ts = files[id][offset:duration]
    if trip_count:
      ts = trips[id][offset:trip_count]
      ts = [item for sublist in ts for item in sublist]

    to_hdf5(ts, id, mdf_input_path, hdf_dir)


main()
