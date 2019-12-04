import argparse
import pathlib
import pandas
import random
import os
import sys
from datetime import datetime
from asammdf import MDF
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips, order_files


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
  if args.duration:
    duration = int(args.duration)
  elif args.trips:
    trip_count = int(args.trips)
  else:
    print('Either sepcifiy duration or amount of trips')
    sys.exit(1)

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
      start_point = random.randrange(0, len(files[id]) - duration)
      temp = files[id]
      temp = temp[start_point:]
      temp = temp[:duration]
      ts = temp
    elif trip_count:
      start_point = random.randrange(0, len(trips[id]) - trip_count)
      ts = trips[id][start_point:trip_count]
      ts = [item for sublist in ts for item in sublist]
    else:
      ts = files[id]

    to_hdf5(ts, id, mdf_input_path, hdf_dir)


main()
